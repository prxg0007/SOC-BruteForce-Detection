# Incident Report (Sample — Filled Out)

## Incident ID
INC-20260717-001

## Title
SSH Brute Force Attack Detected Against victim-vm (labuser account)

## Severity
High

## Date & Time Detected
2026-07-17 09:14 IST

## Reported By / Detected By
[Your Name] / Splunk Alert: "SSH Brute Force - Failed Logins > 10 in 5min"

---

## 1. Summary

Between 09:10 and 09:14 IST, source IP 192.168.56.101 generated 19 failed SSH
login attempts against the `labuser` account on `victim-vm`, followed by one
successful login. This pattern — high-frequency failed attempts with a
successful login shortly after — is consistent with a successful password
brute force attack (MITRE T1110.001).

## 2. Detection Details

- **Alert triggered:** SSH Brute Force - Failed Logins > 10 in 5min
- **Detection query:** `detection_queries/brute_force_detection.spl` (Query 2)
- **Source IP(s) involved:** 192.168.56.101
- **Target account(s):** labuser
- **Number of failed attempts:** 19 (followed by 1 successful login)
- **Time window:** 09:10:02 – 09:14:47 IST

## 3. Investigation Steps Taken

1. Ran Query 3 (`brute_force_detection.spl`) to check for a successful login
   from the flagged IP — confirmed one `Accepted password` event at 09:14:47,
   3 seconds after the 19th failed attempt.
2. Checked average time between attempts using Query 4 — average gap was
   ~2.1 seconds, well below normal human typing speed, confirming this was
   automated (tool-driven) rather than a user mistyping their password.
3. Checked for follow-on activity from `labuser` post-login (sudo commands,
   new SSH keys added, outbound connections) — none observed in this lab run,
   but this step is what you'd repeat against `auth.log`/`sudo` logs in a
   real environment.
4. Searched history for prior activity from 192.168.56.101 — no prior
   sightings; this is a first-time offender IP in this lab.

## 4. Findings

This was a **successful simulated brute force compromise**. The account
`labuser` was accessed by an unauthorized source after 19 failed password
guesses. In a real environment this would be treated as an active compromise
requiring immediate containment, not just monitoring.

## 5. Impact Assessment

- **Confidentiality:** Medium (attacker gained shell access to the account)
- **Integrity:** Low (no evidence of file/config tampering in this lab run)
- **Availability:** None

## 6. Containment & Remediation Actions

- [x] Blocked source IP at firewall (`iptables`/security group rule added)
- [x] Reset password for `labuser`
- [x] Reviewed `~/.ssh/authorized_keys` for unauthorized keys — clean
- [x] Installed and configured `fail2ban` with a 3-attempt/10-minute ban policy
- [x] Disabled password-based SSH authentication in favor of key-based auth
- [ ] MFA — not applicable for local lab SSH, but recommended for any
      externally-facing production system

## 7. Lessons Learned / Recommendations

- Password-only SSH authentication should never be exposed to any network
  the attacker can reach — disable it in favor of SSH keys.
- `fail2ban` (or equivalent) should be a default control on any internet-facing
  Linux host, not an afterthought.
- Alert threshold of 10 failed attempts / 5 minutes worked well here but
  should be tuned against real user behavior to avoid false positives from
  users who genuinely mistype their password a few times.
- In a cloud environment, this same detection maps directly to a GuardDuty
  `UnauthorizedAccess:EC2/SSHBruteForce` finding — see `cloud_extension.md`.

## 8. MITRE ATT&CK Mapping

- **Technique:** T1110 — Brute Force
- **Sub-technique:** T1110.001 — Password Guessing

---
**Analyst Sign-off:** [Your Name] — 2026-07-17
