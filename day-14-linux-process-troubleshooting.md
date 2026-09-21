# Day 14: Linux Process Troubleshooting

**Category:** Linux / Troubleshooting

## Task

Identify the process holding a required port, stop it, and restart the target service (Apache) so it can claim that port.

---

## Solution

### Step 1: Check if the port is in use

```bash
sudo ss -tulnp | grep <port>
```

This shows any listening TCP/UDP socket bound to `<port>`, along with the owning process name and PID.

### Step 2: Identify and stop the conflicting process

Once the owning service is identified from the `ss` output:

```bash
sudo systemctl stop <service>
```

### Step 3: Restart Apache to claim the port

```bash
sudo systemctl restart httpd
```

### Step 4: Verify Apache is now listening on the port

```bash
sudo ss -tulnp | grep <port>
```

Expected: the socket for `<port>` now shows `httpd` as the owning process instead of the previous service.

---

## Key Takeaways

- `ss` is the modern replacement for `netstat` on most current distros — same flags carry over (`-t` TCP, `-u` UDP, `-l` listening, `-n` numeric, `-p` show process/PID), and it's generally faster since it reads directly from kernel sockets rather than `/proc`.
- Grep-ing `ss`/`netstat` output by port number is the fastest way to answer "what's actually using this port" — don't assume based on what a service *should* be doing; verify what's actually bound.
- Stopping the conflicting service only frees the port for the current session — if that service is still `enabled`, it can reclaim the port on the next reboot. Pair `stop` with `disable` if it shouldn't come back automatically.
- Always re-check with `ss`/`netstat` after restarting the target service — a restart can silently fail to bind if something else grabbed the port in between the stop and restart steps.

---

**Stack:** `Linux` `Networking` `Troubleshooting` `Apache`
