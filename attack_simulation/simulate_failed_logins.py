#!/usr/bin/env python3
"""
simulate_failed_logins.py

Generates synthetic Linux auth.log-style SSH brute force entries for use in a
SOC detection lab. Useful when you don't have a second VM / Hydra available,
or you just want a fast, repeatable demo dataset for Splunk.

This does NOT touch any real network or system — it only writes log lines to
a local text file, formatted exactly like real /var/log/auth.log entries, so
Splunk parses them the same way it would parse a live attack.

Usage:
    python3 simulate_failed_logins.py --output demo_auth.log --attempts 40 --success-at 35
"""

import argparse
import random
from datetime import datetime, timedelta

HOSTNAME = "victim-vm"
SSHD_PID = 1234
USERNAME = "labuser"
ATTACKER_IP = "192.168.56.101"


def format_line(ts: datetime, message: str) -> str:
    # Matches standard syslog / auth.log format:
    # Mon DD HH:MM:SS hostname sshd[pid]: message
    return f"{ts.strftime('%b %d %H:%M:%S')} {HOSTNAME} sshd[{SSHD_PID}]: {message}"


def generate_log(output_path: str, attempts: int, success_at: int, start_time: datetime):
    lines = []
    current_time = start_time

    for i in range(1, attempts + 1):
        # Fast, regular intervals -> looks automated (brute force signature)
        current_time += timedelta(seconds=random.uniform(1.5, 3.0))

        if i == success_at:
            msg = f"Accepted password for {USERNAME} from {ATTACKER_IP} port {random.randint(40000,60000)} ssh2"
        else:
            msg = f"Failed password for {USERNAME} from {ATTACKER_IP} port {random.randint(40000,60000)} ssh2"

        lines.append(format_line(current_time, msg))

    with open(output_path, "a") as f:
        f.write("\n".join(lines) + "\n")

    print(f"[+] Wrote {attempts} log lines to {output_path}")
    print(f"[+] Attacker IP used: {ATTACKER_IP}")
    if success_at <= attempts:
        print(f"[+] Simulated successful login at attempt #{success_at}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate synthetic SSH brute-force auth.log entries")
    parser.add_argument("--output", default="demo_auth.log", help="Output log file path")
    parser.add_argument("--attempts", type=int, default=30, help="Total number of login attempts")
    parser.add_argument("--success-at", type=int, default=25, help="Attempt number that succeeds (0 = never)")
    args = parser.parse_args()

    generate_log(args.output, args.attempts, args.success_at, datetime.now())
