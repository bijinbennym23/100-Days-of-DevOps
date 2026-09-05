# Day 4: File Permissions - Making a Script Executable for All Users

**Category:** Linux / File Permissions

## Task

Grant executable permissions to a file and ensure that all users have the capability to execute it.

---

## Solution

### Step 1: Understand the requirement

To make a file executable, it must also be **readable** — a file with only execute permission (`x`) but no read permission (`r`) generally can't be run, since the shell/loader needs to read the file's contents to execute it.

The easiest way to grant read + execute to all users (owner, group, and others) in one shot is:

```bash
sudo chmod +rx xfusioncorp.sh
```

### Step 2: Verify the permissions

```bash
ls -l xfusioncorp.sh
```

Expected output (permission bits should show `r` and `x` set for owner, group, and others):

```text
-rwxr-xr-x 1 root root 0 Aug 28 10:00 xfusioncorp.sh
```

### Step 3: Confirm it runs

```bash
./xfusioncorp.sh
```

---

## Key Takeaways

- `chmod +rx <file>` adds read and execute permissions **for all three permission classes** (user, group, others) without touching write permissions or removing anything already set.
- A file needs **read** permission to be executed, not just execute permission — `chmod +x` alone can leave a file that still can't run if read access is missing.
- `+rx` is symbolic mode syntax and is additive/relative — compare with absolute mode (e.g. `chmod 755 xfusioncorp.sh`), which sets the exact permission bits regardless of what was there before.
- Use `ls -l` to confirm the resulting permission string (`rwxr-xr-x`) rather than assuming the command worked.

---

**Stack:** `Linux` `chmod` `File Permissions`
