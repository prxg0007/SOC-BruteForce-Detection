# Cloud Security Extension — Applying This Lab to AWS / Azure

This project is deliberately built on-prem-style (a local Ubuntu VM) so it's
free, fast, and repeatable without needing a cloud account. But the whole
point of showcasing it for a **cloud security** internship is being able to
clearly explain how every piece maps to a cloud environment. This document is
that mapping — use it verbatim in interviews or as a talking point.

---

## 1. Log Source Mapping

| This Lab | AWS Equivalent | Azure Equivalent |
|---|---|---|
| `/var/log/auth.log` on Ubuntu | CloudWatch Agent shipping OS-level auth logs from EC2, **plus** CloudTrail for API-level auth (`ConsoleLogin`) | Azure Monitor Agent / Log Analytics for VM auth logs, **plus** Azure AD Sign-in Logs |
| SSH brute force against a VM's public IP | Same thing, but against an EC2 instance's public IP/Security Group | Same, against an Azure VM's NSG-exposed IP |
| Splunk `index=main` monitor input | Splunk Add-on for AWS ingesting CloudTrail / VPC Flow Logs / GuardDuty findings via S3 or Kinesis | Splunk Add-on for Microsoft Azure ingesting Activity Logs / Sign-in Logs |

## 2. Detection Mapping

| This Lab | Cloud Equivalent |
|---|---|
| SPL: `count > 10` failed SSH logins by `src_ip` | AWS GuardDuty finding: `UnauthorizedAccess:EC2/SSHBruteForce` (built-in, ML-based) |
| Manual "failed then success" correlation | GuardDuty finding: `UnauthorizedAccess:EC2/RDPBruteForce` or IAM `ConsoleLoginSuccess` after multiple `ConsoleLoginFailure` events in CloudTrail |
| MITRE T1110 mapping | Same MITRE mapping applies — GuardDuty findings are pre-mapped to ATT&CK techniques in the finding details |

## 3. Response/Containment Mapping

| This Lab | Cloud Equivalent |
|---|---|
| `iptables` block on the victim VM | Update EC2 **Security Group** to remove the offending IP's access, or add a deny rule in **Network ACL** |
| Disable password SSH auth | Enforce **key-pair only** access, or better: use **AWS Systems Manager Session Manager** so no SSH port needs to be exposed at all |
| fail2ban | AWS **WAF rate-based rules** (for web-facing brute force) or GuardDuty + Lambda auto-remediation (auto-update Security Group on finding) |

## 4. What a Cloud-Native Version of This Project Looks Like (Your Next Project)

1. Spin up an EC2 instance, enable CloudTrail + VPC Flow Logs.
2. Ingest CloudTrail logs into Splunk (Splunk has a free sample CloudTrail
   dataset if you don't want to pay for real AWS usage: `Splunk_TA_aws` +
   sample data).
3. Detect:
   - Repeated `ConsoleLoginFailure` events from the same IP/user (IAM brute force)
   - `PutBucketAcl` or `PutBucketPolicy` calls that make an S3 bucket public
   - IAM policy changes granting `*:*` permissions (privilege escalation)
4. Build the same detect → alert → investigate → report pipeline as this project.
5. Map each finding to MITRE ATT&CK Cloud Matrix (e.g. T1078.004 — Cloud Accounts).

This gives you two complementary portfolio projects: **on-prem/host-based
detection** (this repo) and **cloud/identity-based detection** (the next one)
— which together cover almost exactly what a SOC/cloud security internship
job description asks for.
