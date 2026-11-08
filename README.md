# Wazuh Alert Summarizer

Reading the raw Wazuh alerts file is painful. Every alert is one giant line of JSON, and most of it isn't what you need. So I wrote a small Python script that pulls out only the parts I care about.

## What it does

It reads the Wazuh alerts file, keeps only the alerts from my two custom SSH rules, and tells me:

- how many alerts there were
- which IP the attack came from
- when the attack started and when it stopped

The rules come from my earlier project, [Wazuh-ssh-bruteforce-detection](https://github.com/Kamal0022/Wazuh-ssh-bruteforce-detection):

- **100010** fires when someone fails SSH login several times from the same IP
- **100011** fires when someone finally gets in after failing several times

The attack these rules look for is **Brute Force (MITRE ATT&CK T1110)**.

## Why it's useful

An analyst looking at a brute-force attack doesn't need every raw alert. They need to know who attacked, how many times, and over what time window. Instead of scrolling through long JSON lines, you get one short summary per attacker IP.

## How it works

1. Opens `/var/ossec/logs/alerts/alerts.json` and reads it one line at a time (each line is one alert).
2. Skips every alert that isn't from rule 100010 or 100011.
3. Turns each matching line into a Python dictionary with `json.loads`.
4. Takes the attacker's IP from `data.srcip`. Not `agent.ip`, which is the machine that reported the alert.
5. Counts alerts per IP and keeps the first and last timestamp for each one.
6. Prints the summary.

## My setup

- Wazuh 4.14 server running in VirtualBox
- Kali Linux as the Wazuh agent (and also the attacker)
- Hydra brute-forcing SSH on Kali itself (`127.0.0.1`)

## How to run it

On the Wazuh server:

```
sudo python3 summarizer.py
```

You need `sudo` because only root can read the alerts file.

## What the output looks like

```
=== SSH Brute-Force Summary ===
Total alerts: 3
IP: 127.0.0.1
 Alerts: 3
 First seen: 2026-11-06T13:41:34.787+0000
 Last seen: 2026-11-06T13:41:38.757+0000
```

## What it can't do (yet)

- It only reads today's alerts file. Wazuh moves older alerts into daily archive files, and the script doesn't read those.
- The file path and rule IDs are written straight into the code.
- In my lab every attack comes from `127.0.0.1`, so you'll only ever see one IP.
- Rule 100011 is in the filter, but it didn't fire in this test, because my Hydra password list didn't have the right password in it.
