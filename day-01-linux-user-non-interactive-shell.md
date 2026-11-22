# Day 1: Linux User Setup with Non-Interactive Shell

**Category:** Linux / User Management

## Task

Create a user named `ravi` on App Server 1 with a **non-interactive shell**, so the account can't be used to log in and run commands.

Reference: [chris-young.net - 1/100 - Linux User Setup with Non-Interactive Shell](https://chris-young.net/1-100/)

---

## Solution

### Step 1: Connect to App Server 1

```bash
ssh tony@172.16.238.10
```

### Step 2: Create the user with a no-login shell

```bash
sudo useradd -s /bin/nologin ravi
```

- `useradd` creates the user.
- `-s /bin/nologin` sets the login shell to `nologin`, a program that refuses interactive logins.
- `ravi` is the username.

### Step 3: Verify

```bash
id ravi
grep '^ravi:' /etc/passwd
```

The last field of the `/etc/passwd` line is the login shell and should read `/bin/nologin`:

```text
ravi:x:1001:1001::/home/ravi:/bin/nologin
```

The exact user and group IDs will differ. To see the shell behave as intended:

```bash
sudo su - ravi
```

It should print a message such as `This account is currently not available.` and return you to your own prompt.

### If `/bin/nologin` doesn't exist

The path varies between distributions. Check which one is present and use it:

```bash
which nologin
ls -l /sbin/nologin /usr/sbin/nologin /bin/false
```

Then use that path with `-s`, for example `/sbin/nologin`, `/usr/sbin/nologin` or `/bin/false`.

---

## Key Takeaways

- **A login shell is just a program that starts when you log in.** Setting it to `nologin` means the session ends immediately after authentication, and no terminal or commands are available through SSH, `su` or a console login.
- **Shell comparison:**

  | Shell path | Allows login? | Behaviour |
  |------------|---------------|-----------|
  | `/bin/bash` | Yes | Full shell access |
  | `/sbin/nologin` | No | Blocks login and prints a "not available" message |
  | `/bin/false` | No | Blocks login silently |

- **This is the standard setup for service accounts.** Daemons such as `nginx`, `mysql` and `www-data` run as users that nobody should log in as, so they get a no-login shell. That limits what an attacker can do if one of those accounts is compromised.
- **It's also useful for limited-access users,** such as someone who only needs to upload files over FTP or SFTP and has no need for a shell.
- **A no-login shell doesn't disable the account.** The user can still own files, run processes and authenticate to services that don't need a shell. To block logins altogether, lock the password (`passwd -l`) or set an expiry date (see Day 2).
- **The path differs between systems.** `/sbin/nologin` is common on RHEL-family distros, and `/usr/sbin/nologin` on Debian and Ubuntu (where `/sbin` and `/usr/sbin` may point to the same place). Check with `which nologin` instead of guessing.
- **Changing the shell later is one command.** `sudo usermod -s /bin/bash ravi` gives the user a real shell, and `sudo chsh -s /bin/nologin ravi` takes it away.
- **Administrators can still act as the user.** `sudo -u ravi <command>` runs a single command as `ravi`, and `sudo su -s /bin/bash ravi` overrides the shell for one session. That's how admins test or run tasks as a service account without giving it a real login shell.

---

**Stack:** `Linux` `User Management` `useradd` `nologin` `Security`
