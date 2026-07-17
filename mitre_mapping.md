# MITRE ATT&CK Mapping

## Primary Technique

**T1110 — Brute Force**
https://attack.mitre.org/techniques/T1110/

> Adversaries may use brute force techniques to gain access to accounts when
> passwords are unknown or when password hashes are obtained.

### Sub-technique used in this lab

**T1110.001 — Password Guessing**
https://attack.mitre.org/techniques/T1110/001/

This lab specifically simulates repeated password guessing against a single
known username (`labuser`) from a single source IP — the classic
"password guessing" pattern rather than password spraying (many usernames,
few passwords each) or credential stuffing (using previously breached
credential pairs).

## Related / Follow-on Techniques (for a real investigation)

| Tactic | Technique | Why it's relevant here |
|---|---|---|
| Initial Access | T1078 — Valid Accounts | Once the password is guessed correctly, the attacker now holds a valid credential |
| Persistence | T1098.004 — SSH Authorized Keys | Check if the attacker added their own SSH key post-compromise |
| Discovery | T1087 — Account Discovery | Attacker may enumerate other accounts on the box after gaining access |
| Command and Control | T1071 — Application Layer Protocol | Check for outbound connections from the compromised account |

## Detection Data Sources (ATT&CK Data Component Mapping)

- **Logon Session Creation** — `sshd` auth.log entries (this lab)
- **User Account Authentication** — Failed/Accepted password events
- In a cloud context: **AWS CloudTrail `ConsoleLogin` events**, **GuardDuty findings**

## Why This Matters for Interviews

Being able to say "this maps to T1110.001, and if it had succeeded, the next
things I'd look for are T1098.004 and T1087" shows you think in terms of
attacker behavior and kill chains, not just isolated alerts. This is a very
common interview question: *"Walk me through what you'd check after this
alert fires."*
