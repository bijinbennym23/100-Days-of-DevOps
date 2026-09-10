# Day 5: SELinux Installation and Configuration

**Category:** Linux / Security

## Task

Install SELinux packages, permanently set SELinux to the `disabled` state in the configuration file, and confirm the change takes effect after the next scheduled reboot.

---

## Solution

### Step 1: Install SELinux packages

### RHEL / CentOS-based systems

```bash
sudo yum install -y selinux-policy selinux-policy-targeted
```

### Debian / Ubuntu-based systems

```bash
sudo apt install -y policycoreutils selinux-basics selinux-utils
```

### Step 2: Edit the SELinux config file

```bash
sudo vi /etc/selinux/config
```

### Step 3: Set SELinux to disabled

Change:

```ini
SELINUX=enforcing
```

to:

```ini
SELINUX=disabled
```

Save and exit (`:wq`).

### Step 4: Verify the change

```bash
grep ^SELINUX= /etc/selinux/config
```

Expected output:

```ini
SELINUX=disabled
```

> **Note:** This config change is **not** live yet — `sestatus` will still show the previous mode until the system reboots. SELinux mode changes to/from `disabled` always require a reboot; unlike `enforcing` ↔ `permissive`, which `setenforce` can toggle at runtime, `disabled` unloads the SELinux policy from the kernel entirely and can only be applied at boot.

---

## Key Takeaways

- `SELINUX=disabled` in `/etc/selinux/config` is a **persistent** setting — it survives reboots.
- The change only takes effect on the **next reboot**, not immediately.
- Package names differ by distro family: `selinux-policy` / `selinux-policy-targeted` (RHEL family) vs. `policycoreutils` / `selinux-basics` / `selinux-utils` (Debian family).
- Confirm actual runtime state post-reboot with `sestatus`, not just by reading the config file.

---

**Stack:** `Linux` `SELinux` `RHEL` `Debian`
