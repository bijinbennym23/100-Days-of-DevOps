# Day 26: Git Manage Remotes

**Category:** Git / Version Control

## Task

In an existing repository, add a new remote pointing at a separate bare repository, then commit a new file and push the `master` branch to that remote.

---

## Solution

### Step 1: Navigate to the repository

```bash
cd /usr/src/kodekloudrepos/news
```

### Step 2: Trust the directory if Git complains about ownership

```bash
git config --global --add safe.directory /usr/src/kodekloudrepos/news
```

This is the same "dubious ownership" fix from Day 24 — needed whenever the repo's owner differs from the user running Git.

### Step 3: Add the new remote

```bash
sudo git remote add dev_news /opt/xfusioncorp_news.git
```

A first attempt pointed the remote at the repo's own working directory (`/usr/src/kodekloudrepos/news`) — that's the wrong target, so it had to be removed before re-adding correctly:

```bash
git remote remove dev_news
```

### Step 4: Verify the remote

```bash
git remote -v
```

Expected output shows `dev_news` with the fetch/push URL `/opt/xfusioncorp_news.git`.

### Step 5: Add a new file and commit it

```bash
sudo cp /tmp/index.html .
sudo git add index.html
sudo git commit -m 'index added'
```

### Step 6: Push master to the new remote

```bash
sudo git push dev_news master
```

---

## Key Takeaways

- A **remote** is just a named alias for a repository URL or path — `origin` is the conventional name for the primary one, but a repo can have any number of remotes with any names (`dev_news` here), which is how you push the same code to multiple destinations.
- The remote must point at a **different** repository than the one you're working in — pointing it at the repo's own directory is a common mix-up. The right target for a shared push destination is normally a bare repo (see Day 21).
- `git remote -v` is the quick sanity check after adding or removing remotes — it lists every remote with its fetch and push URLs, so a wrong path shows up immediately instead of at push time.
- `git push <remote> <branch>` names both explicitly, so the push goes exactly where intended regardless of what the branch's default upstream is set to.
- Running Git commands with `sudo` works when file ownership demands it, but it can leave root-owned files inside `.git/` that later break non-sudo Git commands for the regular user. If you see permission errors afterward, check ownership of the repo directory rather than assuming Git itself is broken.

---

**Stack:** `Git` `Linux` `Version Control`
