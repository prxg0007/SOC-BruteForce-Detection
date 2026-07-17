# Splunk Dashboard — SSH Brute Force Overview

Build these as individual panels in a new Dashboard (Classic or Studio, either
is fine — Studio looks more modern for a portfolio screenshot).

---

## Panel 1: Top Attacking Source IPs (Bar Chart)

```spl
index=main sourcetype=linux_secure "Failed password"
| rex field=_raw "Failed password for (invalid user )?(?<user>\S+) from (?<src_ip>\S+)"
| stats count as failed_attempts by src_ip
| sort - failed_attempts
| head 10
```
Visualization: **Bar Chart**, X-axis = src_ip, Y-axis = failed_attempts

---

## Panel 2: Failed vs Successful Logins Over Time (Line/Area Chart)

```spl
index=main sourcetype=linux_secure ("Failed password" OR "Accepted password")
| eval status=if(match(_raw,"Accepted"),"success","failed")
| timechart span=1m count by status
```
Visualization: **Line Chart**, stacked by `status`

---

## Panel 3: Single Value — Total Alerts Today

```spl
index=main sourcetype=linux_secure "Failed password"
| bucket _time span=5m
| stats count as failed_attempts by src_ip, _time
| where failed_attempts > 10
| stats dc(src_ip) as flagged_ips
```
Visualization: **Single Value**, label: "IPs Flagged for Brute Force (Today)"

---

## Panel 4: Top Targeted Usernames (Pie Chart)

```spl
index=main sourcetype=linux_secure "Failed password"
| rex field=_raw "Failed password for (invalid user )?(?<user>\S+) from (?<src_ip>\S+)"
| top limit=5 user
```
Visualization: **Pie Chart**

---

## Panel 5 (Optional): Attacker Geolocation

If you enable the `iplocation` command (needs GeoIP lookup, built into Splunk):

```spl
index=main sourcetype=linux_secure "Failed password"
| rex field=_raw "Failed password for (invalid user )?(?<user>\S+) from (?<src_ip>\S+)"
| iplocation src_ip
| stats count by src_ip, Country, City
```
Visualization: **Cluster Map**

---

## Screenshot Checklist for Your Portfolio

Take clean screenshots of:
- [ ] The full dashboard with all panels populated
- [ ] The alert configuration screen (showing trigger condition)
- [ ] A triggered alert in the "Triggered Alerts" list
- [ ] The raw SPL search bar with results for Query 2 and Query 3
- [ ] The search job inspector for one query (shows you understand execution, a nice technical touch)

Store them in `/screenshots/` with descriptive names, e.g. `01_dashboard_overview.png`.
