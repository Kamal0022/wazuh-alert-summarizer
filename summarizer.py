import json

counts = {}
first_seen = {}
last_seen = {}

with open("/var/ossec/logs/alerts/alerts.json") as f:
    for line in f:
        if '"id":"100010"' in line or '"id":"100011"' in line:
            alert = json.loads(line)
            ip = alert["data"]["srcip"]
            counts[ip] = counts.get(ip, 0) + 1
            ts = alert["timestamp"]
            if ip not in first_seen:
                first_seen[ip] = ts
            last_seen[ip] = ts

print("=== SSH Brute-Force Summary ===")
print("Total alerts:", sum(counts.values()))
for ip, count in counts.items():
    print("IP:", ip)
    print(" Alerts:", count)
    print(" First seen:", first_seen[ip])
    print(" Last seen:", last_seen[ip])
