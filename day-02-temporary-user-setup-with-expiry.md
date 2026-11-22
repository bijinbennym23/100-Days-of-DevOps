# Day 2: Temporary User Setup with Expiry

**Category:** Linux / User Management

## Task

A developer named `jim` needs access to the Nautilus project for a limited time. On App Server 2 (`172.16.238.12`), create a user account for him that **expires automatically** on `2024-03-28`.

Reference: [chris-young.net - Day 2 of 100](https://chris-young.net/2-100/)

---

## Solution

### Step 1: Connect to the server

```bash
ssh banner@172.16.238.12
```

### Step 2: Create the user with an expiry date

```bash
sudo useradd -e 2024-03-28 jim
```

`-e` (`--expiredate`) sets the date, in `YYYY-MM-DD` format, on which the account becomes disabled.

### Step 3: Verify the expiry date

```bash
sudo chage -l jim
```

Expected output includes:

```text
Account expires						: Mar 28, 2024
```

You can also confirm the account exists:

```bash
id jim
```

### Optional flags

Depending on what the account should be allowed to do, these can be added to the `useradd` command:

| Flag | Effect |
|------|--------|
| `-m` | Creates a home directory (`/home/jim`) |
| `-d /custom/path` | Uses a custom home directory path |
| `-s /sbin/nologin` | Blocks interactive shell login |

For example:

```bash
sudo useradd -e 2024-03-28 -m -s /bin/bash jim
```

---

## Key Takeaways

- **The account is disabled on expiry, not deleted.** After the date passes, `jim` can no longer log in, but his user entry and files stay on the system. That's why `chage -l` is a good way to check the status.
- **To restore access, set a new future date on the existing account.** Use `sudo chage -E 2026-12-31 jim` (or `sudo usermod -e 2026-12-31 jim`). Running `useradd` again would fail, since the user already exists.
- **To remove an expiry completely,** set it to `-1`: `sudo chage -E -1 jim`.
- **Account expiry is different from password expiry.** `useradd -e` and `chage -E` control when the *account* is disabled. Password aging (`chage -M` for max days, `-W` for warning days) controls when the *password* must be changed. A locked-out expired account needs the account date fixed, not a new password.
- **`useradd` vs `adduser`.** `useradd` is the low-level tool available everywhere, and it creates no home directory unless `-m` is given (on most RHEL-family systems it is created by default through `/etc/login.defs`). `adduser` is a friendlier wrapper on Debian and Ubuntu with different options, so the two aren't interchangeable in a command line.
- **Use a future date in real life.** `2024-03-28` is the date given in the lab, and it's already in the past now. An account created with a past expiry date is disabled from the start.
- **Temporary access should always have an end date.** Time-boxed accounts for contractors and short-term developers prevent forgotten, still-active accounts, which is a common audit finding.
- **`/etc/shadow` stores it.** The expiry date is the 8th field, counted as days since 1970-01-01, which is why `chage -l` is easier to read than the file.

---

**Stack:** `Linux` `User Management` `useradd` `chage` `Security`
