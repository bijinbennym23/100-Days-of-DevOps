# Day 32: Git Rebase

**Category:** Git / Version Control

## Task

The Nautilus application development team has been working on a project repository `/opt/beta.git`, cloned at `/usr/src/kodekloudrepos` on the storage server in the Stratos DC. A developer is working on the `feature` branch and their work is still in progress, but some changes have since been pushed to `master`.

Requirements:

1. Rebase `feature` onto `master` without losing any data from `feature`.
2. Don't add a merge commit (so merging `master` into `feature` is not an option).
3. Push the changes once done.

---

## Solution

### Step 1: Connect and move into the repository

```bash
ssh natasha@ststor01
cd /usr/src/kodekloudrepos/beta
```

### Step 2: Trust the directory if Git complains about ownership

```bash
git config --global --add safe.directory /usr/src/kodekloudrepos/beta
```

This is the same "dubious ownership" fix from Day 24.

### Step 3: Fetch the latest state from the remote

```bash
sudo git fetch origin
```

### Step 4: Switch to the feature branch

```bash
sudo git checkout feature
```

### Step 5: Rebase onto master

```bash
sudo git rebase master
```

Git replays each `feature` commit on top of the current tip of `master`, producing a linear history with no merge commit.

### Step 6: Verify the result

```bash
git log --oneline --graph
```

Expected: a single straight line with all the `master` commits first and the `feature` commits stacked on top.

### Step 7: Push the rewritten branch

```bash
sudo git push origin feature --force-with-lease
```

---

## Key Takeaways

- **Rebase vs merge:** `git merge master` ties two histories together with a merge commit. `git rebase master` moves the `feature` commits to start from the new tip of `master`, so the history stays linear. Both bring in the new `master` work and neither loses `feature` changes.
- Rebasing **rewrites** the `feature` commits: they get new hashes because their parent changed. That's why a normal `git push` is rejected afterward and a force push is needed.
- `--force-with-lease` is safer than plain `--force`. It only overwrites the remote branch if it still points where your last fetch saw it, so it won't clobber commits a teammate pushed in the meantime. This is also why the `git fetch origin` step comes first.
- Only rebase branches that others aren't building on. Anyone who already pulled the old `feature` commits will have a diverged history after the force push and will need to reset or rebase their copy.
- If the rebase hits a conflict, Git pauses. Resolve the files, `git add` them, then `git rebase --continue` (or `git rebase --abort` to go back to where you started).
- Run the rebase while **on** the branch being moved (`feature`) and name the branch you're rebasing **onto** (`master`). Getting those backwards is the most common mistake.

---

**Stack:** `Git` `Linux` `Version Control`
