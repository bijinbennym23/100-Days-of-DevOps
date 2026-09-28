# Day 27: Git Revert Some Changes

**Category:** Git / Version Control

## Task

Undo the most recent commit in a repository by creating a new commit that reverses its changes, using a custom commit message.

---

## Solution

### Step 1: Navigate to the repository

```bash
cd /usr/src/kodekloudrepos/blog/
```

### Step 2: Review the history and current state

```bash
git log
git status
```

Confirm which commit is at `HEAD` (the one to be reverted) and that the working tree is clean before starting.

### Step 3: Revert the latest commit without committing yet

```bash
sudo git revert HEAD --no-commit
```

`--no-commit` applies the inverse of the commit's changes to the working tree and index but stops before creating the commit, so the message can be set manually.

### Step 4: Check the staged changes

```bash
sudo git status
```

The reverted changes should appear as staged.

### Step 5: Commit with the required message

```bash
sudo git commit -m 'revert blog'
```

### Step 6: Verify

```bash
git log --oneline
```

Expected: a new commit `revert blog` on top, with the original commit still present below it.

---

## Key Takeaways

- `git revert` **adds a new commit** that undoes an earlier one; it doesn't rewrite history. That makes it the safe choice for commits already pushed or shared, unlike `git reset`, which moves the branch pointer backwards and would force collaborators to reconcile diverged history.
- `--no-commit` (or `-n`) is what allows a custom message: without it, Git opens an editor with a default `Revert "..."` message and commits immediately.
- `HEAD` refers to the latest commit on the current branch; `HEAD~1` would target the one before it. Use `git log` first so the right commit is being reverted, especially if the task names a specific one.
- Reverting a merge commit needs `-m <parent-number>` to say which side to keep. It isn't required for a regular commit like this one.
- If a revert conflicts with later changes, Git stops mid-way and marks the conflicts. Resolve them, `git add` the files, then finish with `git revert --continue` (or `git commit` when using `--no-commit`).

---

**Stack:** `Git` `Linux` `Version Control`
