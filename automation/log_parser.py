#!/usr/bin/env python3
"""
log_parser.py

Standalone Python parser for Linux auth.log SSH brute-force detection.
Demonstrates that detection logic isn't locked inside Splunk — the same idea
(count failed logins per IP, flag over a threshold) can be done with plain
Python. Good talking point in interviews: "I understand the logic, not just
the tool."

Usage:
    python3 log_parser.py --file /var/log/auth.log --threshold 10
"""

import argparse
import re
from collections import defaultdict, Counter

FAILED_RE = re.compile(r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+)")
ACCEPTED_RE = re.compile(r"Accepted password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\S+)")


def parse_log(file_path: str):
    failed_by_ip = defaultdict(int)
    success_by_ip = defaultdict(int)
    user_hits = Counter()

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            fm = FAILED_RE.search(line)
            if fm:
                failed_by_ip[fm.group("ip")] += 1
                user_hits[fm.group("user")] += 1
                continue

            am = ACCEPTED_RE.search(line)
            if am:
                success_by_ip[am.group("ip")] += 1

    return failed_by_ip, success_by_ip, user_hits


def report(failed_by_ip, success_by_ip, user_hits, threshold):
    print("=" * 60)
    print("SSH BRUTE FORCE ANALYSIS REPORT")
    print("=" * 60)

    print(f"\n[Failed login attempts by source IP] (threshold = {threshold})\n")
    flagged = []
    for ip, count in sorted(failed_by_ip.items(), key=lambda x: -x[1]):
        marker = "  <-- ALERT: exceeds threshold" if count > threshold else ""
        if count > threshold:
            flagged.append(ip)
        print(f"  {ip:<20} {count:>5} failed attempts{marker}")

    print(f"\n[Compromise indicators] (flagged IP that later succeeded)\n")
    if not flagged:
        print("  None found.")
    for ip in flagged:
        if success_by_ip.get(ip, 0) > 0:
            print(f"  ⚠ {ip} — {failed_by_ip[ip]} failed attempts THEN a successful login. Likely compromised account.")

    print(f"\n[Top targeted usernames]\n")
    for user, count in user_hits.most_common(5):
        print(f"  {user:<20} {count:>5} attempts")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse auth.log for SSH brute-force indicators")
    parser.add_argument("--file", required=True, help="Path to auth.log (or demo_auth.log)")
    parser.add_argument("--threshold", type=int, default=10, help="Failed attempt count that triggers a flag")
    args = parser.parse_args()

    failed_by_ip, success_by_ip, user_hits = parse_log(args.file)
    report(failed_by_ip, success_by_ip, user_hits, args.threshold)
