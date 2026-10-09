# Day 30: Git Hard Reset

**Category:** Git / Version Control

## Task

Roll a repository back to an earlier commit, discarding everything after it, and update the remote so it matches.

---

## Solution

### Step 1: Connect to the storage server

```bash
ssh natasha@ststor01
sudo su -
```

### Step 2: Navigate to the repository and trust the directory

```bash
cd /usr/src/kodekloudrepos/news/
git config --global --add safe.directory /usr/src/kodekloudrepos/news
```

The `safe.directory` entry is the same "dubious ownership" fix from Day 24.

### Step 3: Find the commit to reset to

```bash
git log --oneline
```

Identify the short hash of the commit that should become the new tip of the branch (here, `02394fa`).

### Step 4: Hard reset to that commit

```bash
git reset --hard 02394fa
```

This moves the branch pointer to `02394fa` and overwrites the index and working tree to match it. Every commit after it drops out of the branch history.

### Step 5: Force-push the rewritten history

```bash
git push --force
```

A normal push is rejected, because the remote still has commits that the local branch no longer contains. `--force` overwrites the remote branch with the local one.

### Step 6: Verify

```bash
git status
git log --oneline
```

Expected: a clean working tree, with `02394fa` at the top of the log and the later commits gone.

---

## Key Takeaways

- `git reset --hard <commit>` is destructive: it moves the branch **and** throws away uncommitted changes in the working tree and index. Run `git status` first, and stash anything you want to keep.
- The discarded commits aren't erased immediately. `git reflog` records where `HEAD` used to point, so a mistaken reset can usually be undone with `git reset --hard <old-hash>` for a while afterward, until Git garbage-collects them.
- Compare with `git revert` (Day 27): revert adds a new commit that undoes an old one and keeps history intact, so it's safe on shared branches. A hard reset **rewrites** history, which is why it forces a force-push.
- `--force` blindly replaces whatever is on the remote, including commits someone else pushed after you last fetched. `git push --force-with-lease` is the safer habit, since it refuses if the remote has moved unexpectedly.
- Rewriting shared history affects everyone who already pulled the old commits: their clones will diverge from the remote and need to reset or rebase. Only do this on a branch where that's acceptable, and tell the team first.
- The other reset modes sit on a spectrum: `--soft` moves only the branch pointer, `--mixed` (the default) also resets the index, and `--hard` resets the working tree as well.

---

**Stack:** `Git` `Linux` `Version Control`
