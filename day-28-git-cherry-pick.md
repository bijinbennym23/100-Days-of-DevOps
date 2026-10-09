# Day 28: Git Cherry Pick Start

**Category:** Git / Version Control

## Task

Apply one specific commit from the `feature` branch onto `master` without merging the whole branch, then push the result to the remote.

---

## Solution

### Step 1: Navigate to the repository and trust the directory

```bash
cd /usr/src/kodekloudrepos/demo
git config --global --add safe.directory /usr/src/kodekloudrepos/demo
```

The `safe.directory` entry is the same "dubious ownership" fix from Day 24.

### Step 2: Find the commit to pick

```bash
git log --oneline
git log --oneline feature
```

Compare the two histories and note the short hash of the commit that exists on `feature` but not on `master` (here, `a048352`).

### Step 3: Switch to the target branch

```bash
sudo git checkout master
```

### Step 4: Cherry-pick the commit

```bash
sudo git cherry-pick a048352
```

### Step 5: Push master to the remote

```bash
sudo git push origin master
```

### Step 6: Verify

```bash
git log --oneline
```

Expected: a new commit on top of `master` with the same message as the picked commit, but a different hash.

---

## Key Takeaways

- `git cherry-pick <hash>` copies the **changes** introduced by one commit and re-applies them as a **new commit** on the current branch. The new commit has a different hash than the original because its parent is different.
- Cherry-picking is for pulling in a single fix or feature without dragging along everything else on the source branch. A `git merge feature` would bring every commit the branches don't share.
- You run it from the **target** branch (`master`), naming the commit that lives on the **source** branch (`feature`). Checking out the wrong branch first is the most common mistake.
- If the change conflicts with what's already on `master`, Git pauses the pick. Resolve the conflicts, `git add` the files, then run `git cherry-pick --continue` (or `--abort` to back out).
- Adding `-x` appends a "(cherry picked from commit ...)" line to the message, which helps trace where a commit came from later.
- The original commit stays on `feature`. If that branch is merged into `master` later, Git may see the same change twice, which usually merges cleanly but is worth knowing about.

---

**Stack:** `Git` `Linux` `Version Control`
