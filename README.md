# 🚨 SOC Detection Lab: SSH Brute Force Detection & Investigation using Splunk

**Author:** Parag Dharmadhikari
**Role Target:** SOC Analyst / Cloud Security Intern
**Tools Used:** Splunk (SIEM), Linux (Ubuntu), Python, Hydra (attack simulation)

---

## 📌 Project Summary

This project simulates a real-world SSH brute force attack against a Linux host,
ingests the resulting authentication logs into Splunk, builds detection logic to
identify the attack, investigates the incident like a SOC analyst, and maps the
findings to the MITRE ATT&CK framework. It also explains how the same detection
logic translates to a cloud environment (AWS/Azure).

**Why this project matters:** it demonstrates the full detection lifecycle —
Log Generation → Ingestion → Detection → Alerting → Investigation → Reporting —
which is the core workflow of a real SOC analyst, not just "I ran some searches."

---

## 🧱 Architecture

```
 Attacker (Kali/local)
        │
        │ SSH brute force attempts
        ▼
 Ubuntu Victim VM
   /var/log/auth.log
        │
        │ Splunk Universal Forwarder / Monitor input
        ▼
   Splunk Search Head (index=main)
        │
        │ SPL detection query
        ▼
   Saved Search → Alert (threshold-based)
        │
        ▼
   Dashboard + Incident Report
```

---

## ⚙️ Step 1 — Environment Setup

- **Victim machine:** Ubuntu VM with OpenSSH server running
- **Attacker machine:** Kali Linux (or another VM) on the same network
- **Splunk:** Installed on victim VM or a separate Splunk instance, ingesting `/var/log/auth.log`

```bash
# On victim VM - confirm SSH is running and logging
sudo systemctl status ssh
tail -f /var/log/auth.log
```

---

## 🧨 Step 2 — Simulate the Attack

Two options are provided in `attack_simulation/`:

1. `hydra_commands.md` — real brute force using Hydra against your **own lab VM only**
2. `simulate_failed_logins.py` — a safe synthetic log generator if you don't want to run live Hydra traffic (useful for quick demos / screenshots)

⚠️ **Ethics note:** Only ever run brute force tools against systems you own or have explicit written permission to test. Never point this at anything on the internet.

---

## 📥 Step 3 — Ingest Logs into Splunk

Splunk → **Settings → Add Data → Monitor**
- Path: `/var/log/auth.log`
- Sourcetype: `linux_secure`
- Index: `main` (or create a dedicated `soc_lab` index)

---

## 🔍 Step 4 — Detection Logic

See `detection_queries/brute_force_detection.spl` for the full set of SPL queries,
including:
- Basic failed login count by source IP
- Threshold-based brute force detection
- Success-after-many-failures (compromise indicator)
- Time-window based detection (velocity)

---

## 🚨 Step 5 — Alerting

Alert configuration (built in Splunk UI, documented here so it's reproducible):

| Setting | Value |
|---|---|
| Search | `brute_force_detection.spl` → Query 2 |
| Trigger condition | `count > 10` in rolling 5 min window |
| Schedule | Run every 5 minutes |
| Action | Add to Triggered Alerts list (+ optional email) |
| Severity | High |

---

## 📊 Step 6 — Dashboard

Panels built (details + SPL in `dashboards/dashboard_panels.md`):
1. Top attacking source IPs (bar chart)
2. Failed vs successful login trend (timechart)
3. Attack timeline (single value + line chart)
4. Geographic map of source IPs (optional, if using iplocation)

---

## 🕵️ Step 7 — Investigation Workflow

Documented step-by-step in `report/incident_report_template.md`, following the
standard SOC triage flow:

1. **Detect** — alert fires for `src_ip` exceeding failed-login threshold
2. **Triage** — confirm it's not a legitimate user locked out of their own account
3. **Investigate** — check if any login from that IP eventually **succeeded**
4. **Correlate** — check for follow-on activity (sudo usage, new user creation, outbound connections) from that account
5. **Contain** — block IP at firewall / security group, disable account if compromised
6. **Document** — fill out the incident report
7. **Lessons learned** — recommend fail2ban / rate limiting / MFA

A filled-out **sample incident report** is included at
`report/sample_incident_report.md` so you can see exactly how to write one.

---

## 🌍 Step 8 — Cloud Relevance (AWS / Azure)

See `cloud_extension.md` for the full write-up. Short version:

| On-Prem Concept | Cloud Equivalent |
|---|---|
| `/var/log/auth.log` on Ubuntu | CloudTrail (API-level) + OS logs via CloudWatch Agent on EC2 |
| SSH brute force to a VM | Brute force against EC2 public IP, or `ConsoleLogin` brute force in CloudTrail |
| Splunk `index=main` search | Splunk Add-on for AWS ingesting CloudTrail/VPC Flow Logs |
| IP-based alert | GuardDuty finding: `UnauthorizedAccess:EC2/SSHBruteForce` |
| Manual IP block | Update Security Group / NACL, or AWS WAF rule |

---

## 🎯 MITRE ATT&CK Mapping

See `mitre_mapping.md`. Primary technique: **T1110 – Brute Force** (sub-technique T1110.001 – Password Guessing).

---

## 🧰 Automation

`automation/log_parser.py` — a Python script that parses `auth.log` directly
(independent of Splunk) and prints top offending IPs + failed attempt counts.
This shows you can work with raw logs, not just a GUI.

---

## 📁 Repository Structure

```
SOC-BruteForce-Detection/
│
├── README.md
├── detection_queries/
│   └── brute_force_detection.spl
├── dashboards/
│   └── dashboard_panels.md
├── attack_simulation/
│   ├── hydra_commands.md
│   └── simulate_failed_logins.py
├── automation/
│   └── log_parser.py
├── report/
│   ├── incident_report_template.md
│   └── sample_incident_report.md
├── mitre_mapping.md
├── cloud_extension.md
└── screenshots/          
```

---

## ✅ Skills Demonstrated

- Log source onboarding in Splunk
- SPL detection engineering (stats, eval, where, transaction)
- Alert creation and tuning (false-positive awareness)
- Dashboard building
- Incident investigation and reporting (SOC workflow)
- MITRE ATT&CK mapping
- Python log parsing / automation
- Cloud security translation (AWS CloudTrail / GuardDuty equivalents)


