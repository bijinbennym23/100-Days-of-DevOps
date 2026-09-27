# Day 21: Set Up Git Repository on Storage Server

**Category:** Git / Version Control

## Task

Install Git on the storage server and initialize a bare repository that other machines can push to and pull from — the standard pattern for a self-hosted, centralized Git remote.

---

## Solution

### Step 1: Install Git

```bash
sudo su -
dnf install git -y
```

### Step 2: Initialize a bare repository

```bash
git init --bare /opt/blog.git
```

### Step 3: Verify the repository was created

```bash
ls -la /opt/blog.git
```

Expected: a directory structure with `HEAD`, `config`, `objects/`, `refs/`, etc. — no working tree files, since a bare repo holds only Git's internal data.

### Step 4: Clone/push from a client machine

From a developer machine (over SSH, assuming the storage server is reachable):

```bash
git clone user@storage-server:/opt/blog.git
```

Or, to point an existing local repo at it as a remote:

```bash
git remote add origin user@storage-server:/opt/blog.git
git push origin main
```

---

## Key Takeaways

- `git init --bare` creates a repository with **no working directory** — it holds only the `.git` internals (normally hidden inside `.git/` in a regular repo) directly at the top level. This is the correct choice for a repo meant to be a shared remote, since nobody edits files directly on the server; they clone, commit locally, and push.
- Using a **regular** (non-bare) `git init` for a shared remote is a common mistake — pushing to a non-bare repo's currently checked-out branch is refused by default (or silently doesn't update the working tree), because Git can't safely reconcile a push with an active working directory on the receiving end.
- Bare repos conventionally use a `.git` suffix in the directory name (`blog.git`) to signal at a glance that it's a bare repo/remote, not a regular working copy.
- Access to a repo like this is typically via SSH (`user@host:/path/to/repo.git`) — which means the SSH key setup from Day 7 is directly relevant here: passwordless key-based auth is what makes `git push`/`git pull` against this remote non-interactive.
- No further "server" process is required for this to work over SSH — Git uses the `git-upload-pack`/`git-receive-pack` commands invoked over the SSH session itself, unlike protocols such as the Git daemon or `git http-backend`, which need a dedicated service running.

---

**Stack:** `Git` `Linux` `Version Control` `SSH`
