# Day 9: MariaDB Troubleshooting

**Category:** Linux / Databases / Troubleshooting

## Task

A production application is down. The support team has traced the root cause to the MariaDB service not running on the database server — diagnose and fix it.

---

## Solution

### Step 1: Try starting the service and check its status

```bash
sudo su -
systemctl start mariadb
```

The start fails. Check why:

```bash
systemctl status mariadb
```

An `Exit status: 1 (FAILURE)` here typically points to a permissions problem or a missing directory, not a config syntax error.

### Step 2: Check the data directory

```bash
ls -ld /var/lib/mysql
```

Confirm the directory exists and is owned by `mysql:mysql` with proper read/write/execute permissions. If this comes back clean, the problem lies elsewhere.

### Step 3: Check the MariaDB error log

```bash
tail -30 /var/log/mariadb/mariadb.log
```

The log reveals the actual failure:

```text
[ERROR] mariadbd: Can't create/write to file '/run/mariadb/mariadb.pid' (Errcode: 13 "Permission denied")
[ERROR] Can't start server: can't create PID file: Permission denied
```

### Step 4: Fix ownership and permissions on the runtime directory

The problem isn't `/var/lib/mysql` — it's `/run/mariadb`, the runtime directory where the PID file lives:

```bash
chown -R mysql:mysql /run/mariadb
chmod 755 /run/mariadb
```

### Step 5: Restart and verify

```bash
systemctl start mariadb
systemctl status mariadb
```

MariaDB should now start successfully.

---

## Key Takeaways

- A `systemctl status` failure code alone rarely tells the full story — the actual service log (here, `/var/log/mariadb/mariadb.log`) is where the real cause shows up. Don't stop investigating at the exit code.
- `/run/` (and `/var/run/` on older systems) is often a `tmpfs` that gets recreated on every boot — permissions on runtime directories under it can silently reset after a reboot even if they were correctly set before, which is why this class of failure tends to reappear intermittently rather than being a one-time fix.
- The visible symptom (data directory `/var/lib/mysql`) and the actual cause (`/run/mariadb` PID file permissions) were two different locations — checking the "obvious" directory first and finding it clean is still useful diagnostic information, since it rules out one possibility and narrows the search.
- `chown -R` recurses through every file and subdirectory under the target path — necessary here since the PID file and potentially other runtime files under `/run/mariadb` all need `mysql:mysql` ownership, not just the top-level directory.
- Some readers of the original writeup pointed out that if `/var/lib/mysql` doesn't exist at all (rather than existing with wrong permissions), a separate fix is needed first — typically `mariadb-install-db` (or the older `mysql_install_db`) to initialize the data directory, rather than just `mkdir -p`. Worth checking which situation actually applies before assuming a permissions-only fix will be enough.

---

**Stack:** `Linux` `MariaDB` `systemd` `Troubleshooting`
