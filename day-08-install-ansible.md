# Day 8: Install Ansible

**Category:** Automation / Configuration Management

## Task

Install a specific version of Ansible (v4.10.0) globally via `pip3`, ensuring `pip3` itself is present and up to date first.

---

## Solution

### Step 1: Ensure pip3 is installed

```bash
sudo yum install -y python3-pip
```

### Step 2: Upgrade pip

```bash
sudo pip3 install --upgrade pip
```

### Step 3: Install Ansible v4.10.0 globally

```bash
sudo /usr/local/bin/pip3 install ansible==4.10.0
```

Pinning the version with `==4.10.0` avoids pulling in whatever the latest release happens to be — important when a playbook/module set is tested against a specific Ansible version.

### Step 4: Verify the installation

```bash
ansible --version
```

Expected output includes the installed version:

```text
ansible [core 2.11.x]
  ...
```

> **Note:** Ansible 4.10.0 is a community package version that wraps `ansible-core` 2.11.x — `ansible --version` will show the underlying core version, not `4.10.0` directly. That's expected and confirms the install matches.

---

## Key Takeaways

- `sudo pip3 install --upgrade pip` before installing packages avoids failures caused by an outdated pip not resolving newer package metadata correctly.
- Pinning with `package==version` (rather than a bare `pip3 install ansible`) guarantees a reproducible install across environments — critical for CI runners and provisioning scripts where "works on my machine" isn't good enough.
- Calling the full path `/usr/local/bin/pip3` instead of just `pip3` avoids ambiguity when multiple `pip3` binaries exist on `$PATH` (e.g. a system one vs. one from a Python version manager).
- Ansible's own version numbering (4.x, 5.x, 6.x) is decoupled from `ansible-core`'s version — always check `ansible --version` output rather than assuming a 1:1 match with the pip-installed version string.

---

**Stack:** `Ansible` `Python` `pip` `Configuration Management`
