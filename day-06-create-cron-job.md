# Day 6: Create a Cron Job

**Category:** Linux / Scheduling

## Task

Add a cron job that runs every 5 minutes and writes `hello` to `/tmp/cron_text`, scheduled under the `root` user.

---

## Solution

### Step 1: Open root's crontab for editing

```bash
sudo crontab -u root -e
```

### Step 2: Add the cron entry

```text
*/5 * * * * echo hello > /tmp/cron_text
```

Save and exit the editor (crontab validates syntax on save and will reject a malformed line).

### Step 3: Verify the entry was saved

```bash
sudo crontab -u root -l
```

Expected output:

```text
*/5 * * * * echo hello > /tmp/cron_text
```

### Step 4: Confirm it's running

Wait for the next 5-minute boundary, then check:

```bash
cat /tmp/cron_text
```

Expected output:

```text
hello
```

---

## Key Takeaways

- Cron schedule fields are `minute hour day-of-month month day-of-week`. `*/5 * * * *` means "every 5 minutes, every hour, every day" — the `*/N` step syntax applies within the allowed range for that field.
- `crontab -u root -e` edits **root's** crontab specifically — running plain `crontab -e` (without `sudo`) edits the current user's own crontab instead, which is a common mix-up.
- `>` **overwrites** `/tmp/cron_text` on every run, so the file only ever holds the latest run's output. Use `>>` instead if you want to append and keep a history across runs.
- `crontab -l` is the safe way to confirm what's actually scheduled, rather than assuming the edit was saved correctly.

---

**Stack:** `Linux` `Cron` `Scheduling`
