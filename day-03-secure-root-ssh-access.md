# Day 3: Secure Root SSH Access

**Category:** Linux / Security

## Task

Following a security audit, direct SSH login as `root` must be disabled on all app servers in the Datacenter, so nobody can connect to them as `root` over SSH. The servers are `stapp01`, `stapp02` and `stapp03`.

Reference: [chris-young.net - Day 3 of 100](https://chris-young.net/3-100/)

---

## Solution

*(Repeat on each app server. Example uses `stapp01`.)*

### Step 1: Connect with your personal user

```bash
ssh tony@stapp01
```

Use the regular user for each server (`tony` on `stapp01`, `steve` on `stapp02`, `banner` on `stapp03`). Root login is what's being turned off, so connect as a normal user with `sudo` rights.

### Step 2: Open the SSH daemon config

```bash
sudo vi /etc/ssh/sshd_config
```

### Step 3: Disable root login

Find the `PermitRootLogin` line. It's commented out by default (`#PermitRootLogin yes`). Remove the `#` and set the value to `no`:

```text
PermitRootLogin no
```

Save and exit (`Esc`, then `:wq`).

### Step 4: Check the config syntax

```bash
sudo sshd -t
```

No output means the file is valid. This catches typos before they can stop the SSH service from restarting.

### Step 5: Restart the SSH service

```bash
sudo systemctl restart sshd
```

### Step 6: Verify

Check that the service came back up:

```bash
sudo systemctl status sshd
```

It should show `active (running)`. Then check the effective setting:

```bash
sudo sshd -T | grep -i permitrootlogin
```

Expected output:

```text
permitrootlogin no
```

From another machine (for example the jump host), a root login attempt should now be refused:

```bash
ssh root@stapp01
```

The result should be `Permission denied`, even with the correct password.

### Step 7: Repeat on the other servers

Do Steps 1 to 6 on `stapp02` and `stapp03`.

---

## Key Takeaways

- **Root is the most targeted account.** Every Linux system has a `root` user, so attackers know the username already and only need to guess the password. Disabling direct root login removes that target and forces an attacker to find a second, valid username as well.
- **It improves accountability.** With root login off, admins connect as themselves and escalate with `sudo`, so the logs show *who* ran each privileged command instead of an anonymous `root`.
- **`PermitRootLogin` has more than two values.** `no` blocks root logins completely. `prohibit-password` (the default in recent OpenSSH) allows root only with a key. `forced-commands-only` allows keys only to run a pre-set command. `yes` allows everything.
- **A commented line is the default, not a setting.** `#PermitRootLogin yes` shows an old default as documentation, and the real default depends on the OpenSSH version. Uncomment the line and set it explicitly so the intent is clear.
- **Restart, or reload, to apply it.** `sshd` reads its config only at start, so edits have no effect until `systemctl restart sshd` (or `reload`). Existing sessions stay connected through a restart, so test a new login separately.
- **Don't lock yourself out.** Before closing your session, confirm that your normal user can log in and use `sudo`. Keep the original session open while testing, because a bad `sshd_config` or a missing sudo user on a remote server can be hard to recover from.
- **`sshd -t` validates and `sshd -T` shows the effective config.** The second one prints the settings sshd will actually use, including defaults and anything pulled in from `sshd_config.d/`, which is more reliable than reading the file.
- **Drop-in files can override the main file.** On newer distributions, files in `/etc/ssh/sshd_config.d/*.conf` are read too, and the first value found for a directive wins. If `sshd -T` still shows the old value, check that directory.

---

**Stack:** `Linux` `SSH` `sshd` `Security` `Hardening`
