# Day 7: Linux SSH Authentication

**Category:** Linux / Networking

## Task

Set up SSH key-based authentication: check for existing SSH keys, generate a new key pair if needed, and copy the public key to target servers for passwordless login.

---

## Solution

### Step 1: Check for existing SSH keys

```bash
ls ~/.ssh/
```

Look for existing key pairs (e.g. `id_rsa` / `id_rsa.pub`, `id_ed25519` / `id_ed25519.pub`) before generating new ones — reusing an existing key avoids unnecessarily managing multiple keys across servers.

### Step 2: Generate a new SSH key pair

```bash
ssh-keygen -t rsa -N "" -f ~/.ssh/id_rsa
```

- `-t rsa` — key type (RSA).
- `-N ""` — empty passphrase, so the key can be used non-interactively (e.g. in scripts/automation). Skip `-N ""` and it'll prompt for a passphrase instead, which is the more secure choice for interactive/manual use.
- `-f ~/.ssh/id_rsa` — output path/filename for the private key (`id_rsa.pub` is generated alongside it).

### Step 3: Copy the public key to each target server

```bash
ssh-copy-id <user>@<server-ip>
```

This appends the local public key (`~/.ssh/id_rsa.pub` by default) to `~/.ssh/authorized_keys` on the remote server for `<user>`, prompting once for that user's password to authenticate the copy.

### Step 4: Verify passwordless login works

```bash
ssh <user>@<server-ip>
```

Should log in directly without a password prompt.

---

## Key Takeaways

- Always check for existing keys first — generating a new pair when one already exists (and is already trusted on other servers) creates unnecessary key sprawl.
- `-N ""` trades security for automation convenience; a passphrase-protected key is safer but requires `ssh-agent` for non-interactive use.
- `ssh-copy-id` handles directory/file permissions (`~/.ssh`, `authorized_keys`) correctly on the remote end — appending manually via `cat id_rsa.pub | ssh ... "cat >> ~/.ssh/authorized_keys"` risks getting those permissions wrong, which SSH will silently reject.
- `authorized_keys` must be `600` and `~/.ssh` must be `700` on the remote server, or SSH will refuse to use the key regardless of whether it's present.

---

**Stack:** `Linux` `SSH` `Networking` `Security`
