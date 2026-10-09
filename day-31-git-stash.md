# Day 31: Git Stash

**Category:** Git / Version Control

## Task

A developer on the Nautilus team stashed some in-progress changes in a repository on the Storage server. Find the stash entry identified as `stash@{1}`, restore it, then commit the restored changes and push them to the origin.

---

## Solution

### Step 1: Connect and move into the repository

```bash
ssh natasha@ststor01
sudo su -
cd /usr/src/kodekloudrepos/media/
```

### Step 2: List the stashes and inspect the target one

```bash
git stash list
git stash show stash@{1}
```

`git stash show` prints a summary of the files the stash touches, so you can confirm it's the right entry before applying it.

### Step 3: Switch to master and apply the stash

```bash
git checkout master
git stash apply stash@{1}
git status
```

`git status` should now list the restored changes as modified or new files.

### Step 4: Commit the restored changes

```bash
git add .
git commit -m 'Restored stashed changes from stash@{1}'
git log --oneline -n 1
```

### Step 5: Push to the origin

```bash
git remote -v
git push origin master
```

### Step 6: Verify on the remote

```bash
cd /opt/media.git && git log --oneline master
```

The new commit should be at the top of the log in the bare repository.

---

## Key Takeaways

- `git stash apply` restores the changes but **keeps** the stash entry in the list. `git stash pop` applies and then drops it. Using `apply` is safer when you want to confirm the result before the stash disappears.
- Stash entries are numbered newest-first: `stash@{0}` is the most recent, so `stash@{1}` is the second most recent. Always run `git stash list` and `git stash show` first, because applying the wrong index restores the wrong work.
- Applying a stash can conflict with changes on the current branch. If that happens, resolve the conflicts, stage the files, and commit as usual. The stash entry is kept, so nothing is lost.
- The `{1}` in `stash@{1}` can be interpreted by some shells (zsh in particular) as a glob or brace expansion. Quote it (`'stash@{1}'`) if the command errors out.
- Stashes are local to a clone and are never pushed. The way to share restored work is the commit and push at the end of the task.
- Checking the bare repository's log after the push confirms the commit actually reached the remote, which is a better test than trusting the push output alone.

---

**Stack:** `Git` `Linux` `Version Control`
