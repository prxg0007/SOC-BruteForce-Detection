# Incident Report

## Incident ID
INC-20260717-001

## Title
SSH Brute Force Attack Against victim-vm — Successful Compromise of the `admin` Account from 172.16.0.3

## Severity
High

## Date & Time Detected
2026-07-17 23:27:09 IST (real-time trigger of alert "SSH Brute Force Detection - Failed Logins")

## Reported By / Detected By
Parag Dharmadhikari / Splunk Alert: "SSH Brute Force Detection - Failed Logins"

---

## 1. Summary

Between approximately 22:30 IST and 23:30 IST on 2026-07-17, four distinct
source IPs (`10.0.0.5`, `172.16.0.3`, `192.168.1.20`, `192.168.1.10`)
generated a combined 57 failed SSH login attempts against `victim-vm` in two
separate bursts, targeting the common usernames `admin`, `test`, `root`, and
`user`. One of the four IPs, `172.16.0.3`, went on to authenticate
**successfully** as `admin` after 7 failed attempts against that account —
confirming an actual (simulated) credential compromise, not just noisy
scanning. The real-time Splunk alert correctly fired during the second burst.

## 2. Detection Details

- **Alert triggered:** SSH Brute Force Detection - Failed Logins (real-time alert, triggered 2026-07-17 23:27:09 IST)
- **Detection query:** `detection_queries/brute_force_detection.spl` — Query 2 (alert base query, 5‑minute bucketed failed-login count) and Query 3 (failed+success compromise indicator)
- **Source IP(s) involved:**

  | Source IP | Total failed attempts | Avg. time between attempts |
  |---|---|---|
  | 10.0.0.5 | 19 | ~200.6s |
  | 192.168.1.20 | 14 | ~272.3s |
  | 172.16.0.3 | 12 | ~317.7s |
  | 192.168.1.10 | 12 | ~317.7s |

- **Target account(s):** `admin` (23 attempts / 40.4%), `test` (14 / 24.6%), `root` (11 / 19.3%), `user` (9 / 15.8%) — 57 failed attempts total across all source IPs (Query 6)
- **Number of failed attempts:** 57 failed, 1 successful (Query 5 timechart)
- **Time window:** two distinct bursts — ~22:30:00 IST and ~23:25:00–23:30:00 IST — all activity confined to two 1-minute windows per the Query 5 timechart, consistent with scripted/automated tooling rather than a human typing

## 3. Investigation Steps Taken

1. Ran Query 2 (5-minute bucketed failed-login count) and confirmed multiple
   source IPs exceeded the alert threshold in the same time buckets
   (`172.16.0.3`: 6, `192.168.1.20`: 6, `192.168.1.10`: 4 at 23:30:00 IST;
   `10.0.0.5`: 10 and 6 across the 22:30 and 23:25 buckets) — ruled out a
   single legitimate user simply mistyping their password, since the volume
   and multi-account targeting pattern is inconsistent with normal behavior.
2. Ran Query 3 (failed + success correlation) to check whether any flagged IP
   also achieved a successful login. Result: `172.16.0.3` recorded 7 failed
   attempts against `admin` followed by 1 successful authentication —
   confirming this was not just a noisy scan but an actual compromise.
3. Ran Query 4 (attack velocity / average gap between attempts) for all four
   IPs. All four averaged well under 6 minutes between attempts across a
   ~1 minute attack window, and `10.0.0.5` was both the fastest (lowest
   average gap) and highest-volume attacker (19 attempts) — strong
   confirmation of automated, tool-driven brute forcing rather than manual
   login attempts.
4. Reviewed Query 6 (top targeted usernames) and found the attack targeted
   four common/default usernames (`admin`, `root`, `test`, `user`) rather
   than a single known account — indicating this campaign behaves more like
   broad password guessing against likely default accounts than a targeted
   attack on one known user.
5. Checked for follow-on activity (sudo usage, new SSH keys, outbound
   connections) from the compromised `admin` session — none observed in this
   lab run, but this is the step to repeat against `auth.log`/`sudo` logs in
   a live environment before an incident can be closed.
6. Confirmed alert fidelity: the real-time alert "SSH Brute Force Detection -
   Failed Logins" triggered at 23:27:09 IST, which falls inside the second
   (23:25–23:30) attack burst — the alert fired during the live attack
   rather than only after the fact.

## 4. Findings

This was a **successful simulated brute force compromise**. Source IP
`172.16.0.3` obtained valid credentials for the `admin` account on
`victim-vm` after only 7 failed password guesses, evidenced by Query 3's
correlated `failed_count=7, success_count=1` result. Three other IPs
(`10.0.0.5`, `192.168.1.20`, `192.168.1.10`) conducted parallel brute-force
attempts against the same host but were **not** observed to succeed. In a
production environment, this would be escalated and handled as an active,
confirmed compromise on `admin` — not a monitoring-only event — while the
other three IPs would still be blocked and tracked as active threat
indicators.

## 5. Impact Assessment

- **Confidentiality:** Medium — attacker (`172.16.0.3`) obtained valid
  `admin` credentials and shell access to `victim-vm`.
- **Integrity:** Low — no evidence of file, configuration, or `sudoers`
  tampering was observed in this lab run; a full post-compromise review of
  `auth.log`, `sudo` logs, and `~/.ssh/authorized_keys` is still required.
- **Availability:** None — no denial-of-service or resource exhaustion
  observed from any of the four source IPs.

## 6. Containment & Remediation Actions

- [x] Blocked source IP `172.16.0.3` (confirmed compromise) at firewall / security group
- [x] Blocked `10.0.0.5`, `192.168.1.20`, `192.168.1.10` as active brute-force indicators
- [x] Reset password for the `admin` account
- [x] Reviewed `~/.ssh/authorized_keys` for unauthorized keys — clean
- [x] Installed and configured `fail2ban` with a low attempt/ban-window policy
- [x] Disabled password-based SSH authentication in favor of key-based auth
- [ ] MFA — not applicable to this local lab, but recommended for any
      internet-facing production system

## 7. Lessons Learned / Recommendations

- The attack targeted default/common usernames (`admin`, `root`, `test`,
  `user`) rather than a single known account — default and shared-sounding
  usernames should be disabled or renamed on any exposed host.
- Password-only SSH authentication should never be reachable from a network
  an attacker can access; disable it in favor of SSH keys.
- `fail2ban` (or an equivalent rate-limiting control) should be a default
  control on any internet-facing Linux host, not an afterthought — in this
  incident, 3–7 failed attempts were enough to succeed, well under the
  Query 2 alert threshold, which means **the alert detected the attack but
  would not have prevented the compromise on its own.**
- The current alert threshold (>3 failed logins per 5‑minute window, per
  Query 2) is appropriately sensitive for a lab, but should be validated
  against real user behavior in production to balance detection speed
  against false positives from genuine mistyped passwords.
- Multiple source IPs attacking the same host in the same short window is
  itself a signal worth its own correlation search/alert (e.g., distinct
  source IP count against one destination host within N minutes), rather
  than relying solely on a per-IP threshold.
- In a cloud environment, this same detection maps directly to a GuardDuty
  `UnauthorizedAccess:EC2/SSHBruteForce` finding — see `cloud_extension.md`.

## 8. MITRE ATT&CK Mapping

- **Technique:** T1110 — Brute Force
- **Sub-technique:** T1110.001 — Password Guessing
- **Follow-on (post-compromise) techniques to check for:** T1078 — Valid
  Accounts (attacker now holds a valid `admin` credential), T1098.004 — SSH
  Authorized Keys (persistence), T1087 — Account Discovery
- See `mitre_mapping.md` for full mapping and data source references.

---
**Analyst Sign-off:** [Parag Dharmadhikari] — 2026-07-17
