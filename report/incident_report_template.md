# Incident Report Template

## Incident ID
INC-[YYYYMMDD]-[001]

## Title
[e.g. SSH Brute Force Attack Detected Against victim-vm]

## Severity
[Low / Medium / High / Critical]

## Date & Time Detected
[Timestamp of first alert trigger]

## Reported By / Detected By
[Your name] / Splunk Alert: [alert name]

---

## 1. Summary

Brief 2-3 sentence description of what happened.

## 2. Detection Details

- **Alert triggered:** [alert name]
- **Detection query:** [link to SPL query used]
- **Source IP(s) involved:** [IP address(es)]
- **Target account(s):** [username(s)]
- **Number of failed attempts:** [count]
- **Time window:** [start time] – [end time]

## 3. Investigation Steps Taken

1. Confirmed alert was not a false positive (e.g. legitimate user locked out) by checking [what you checked].
2. Searched for successful logins from the same source IP: [result].
3. Checked for follow-on activity (sudo commands, new users, cron jobs, outbound connections) from the target account: [result].
4. Reviewed historical activity from this source IP to determine if this is a repeat offender: [result].

## 4. Findings

[State clearly: Was this a successful compromise, an unsuccessful attack, or a false positive? What is the evidence?]

## 5. Impact Assessment

- **Confidentiality:** [None / Low / Medium / High]
- **Integrity:** [None / Low / Medium / High]
- **Availability:** [None / Low / Medium / High]

## 6. Containment & Remediation Actions

- [ ] Blocked source IP at firewall / security group
- [ ] Disabled or reset password for affected account
- [ ] Reviewed authorized_keys / sudoers for tampering
- [ ] Enabled fail2ban / rate limiting
- [ ] Enforced key-based SSH authentication (disable password auth)
- [ ] Enabled MFA where applicable

## 7. Lessons Learned / Recommendations

[e.g. Recommend disabling password-based SSH auth entirely, tightening security group rules to allow SSH only from known IP ranges, deploying fail2ban, lowering the alert threshold.]

## 8. MITRE ATT&CK Mapping

- **Technique:** T1110 — Brute Force
- **Sub-technique:** T1110.001 — Password Guessing

---
**Analyst Sign-off:** [Your Name] — [Date]
