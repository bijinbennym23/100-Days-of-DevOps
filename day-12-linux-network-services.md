# Day 12: Linux Network Services

**Category:** Linux / Networking

## Task

Connect to a server, confirm whether `httpd` (Apache) is running, check what's actually listening on its port, and — if a conflicting service like `sendmail` is holding the port — stop it and get `httpd` running.

---

## Solution

### Step 1: Connect to the server

```bash
ssh tony@stap01
```

### Step 2: Check whether httpd is running

```bash
systemctl status httpd
```

### Step 3: Check what's listening on Apache's port

```bash
netstat -tlpn
```

This shows all listening TCP sockets along with the PID/process name bound to each port — useful for spotting whether something *other* than `httpd` has already claimed the port `httpd` needs.

### Step 4: Stop the conflicting service and start httpd

If another service (e.g. `sendmail`) is occupying the port `httpd` needs:

```bash
sudo systemctl stop sendmail
sudo systemctl restart httpd
sudo systemctl status httpd
```

---

## Key Takeaways

- `systemctl status <service>` failing to start silently is often a **port conflict**, not a config problem — always check `netstat -tlpn` (or `ss -tlpn` on newer systems) before assuming the service itself is broken.
- `netstat -tlpn` flags: `-t` (TCP), `-l` (listening sockets only), `-p` (show the owning process/PID — requires root to see other users' processes), `-n` (numeric addresses/ports, skips slow DNS/service-name lookups).
- Stopping a conflicting service only fixes the *current* boot — if it's enabled, it can come back and reclaim the port on the next reboot. Use `sudo systemctl disable <service>` alongside `stop` if it shouldn't start automatically anymore.
- `systemctl restart` (rather than `start`) is the safer choice for httpd here — it ensures a full stop/start cycle even if httpd was left in a partially-started or failed state from the earlier port conflict.

---

**Stack:** `Linux` `systemd` `Networking` `Apache`
