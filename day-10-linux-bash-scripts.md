# Day 10: Linux Bash Scripts

**Category:** Linux / Bash Scripting

## Task

Write a bash script (run as the current user) that archives a web app directory and transfers the backup to a remote backup server via `scp`, using key-based SSH auth so the transfer runs non-interactively.

Reference: [tundedamian - Day 10 of 100 Days of DevOps](https://tundedamian.medium.com/day-10-of-100-days-of-devops-e68b5a0fe8e2)

---

## Solution

### Step 1: Set up key-based SSH auth to the backup server

```bash
ssh-keygen
ssh-copy-id clint@stbkp01
```

This is a prerequisite, not part of the script itself — the script's `scp` step needs to run without a password prompt, so the key must already be trusted on `stbkp01` before the script is scheduled or automated (same pattern as Day 7).

### Step 2: Write the backup script

```bash
#!/bin/bash

# Step 1: Create zip archive
zip -r /backup/xfusioncorp_blog.zip /var/www/html/blog

# Step 2: Transfer backup to remote backup server (stbkp01)
scp /backup/xfusioncorp_blog.zip clint@stbkp01:/backup
```

### Step 3: Make the script executable and run it

```bash
chmod +x backup.sh
./backup.sh
```

### Step 4: Verify the backup arrived

On `stbkp01`:

```bash
ls -l /backup/xfusioncorp_blog.zip
```

---

## Key Takeaways

- The script runs as the **current user**, not root — so `ssh-copy-id` must be run as that same user, and the local `/backup` directory and remote `/backup` path both need to be writable by that user, not just by root.
- `zip -r` recurses into the source directory to include all files/subdirectories — a bare `zip` (no `-r`) on a directory only creates an empty or partial archive.
- Because SSH key auth is already set up, `scp` here runs non-interactively — this is what makes the script safe to drop into `cron` (see Day 6) for scheduled backups, rather than needing manual password entry every run.
- Always test the script manually once (`./backup.sh`) before wiring it into cron — a script that silently fails on a schedule (e.g. due to a missing key or wrong path) is much harder to debug than one that fails in front of you.

---

**Stack:** `Linux` `Bash` `SSH` `SCP` `Automation`
