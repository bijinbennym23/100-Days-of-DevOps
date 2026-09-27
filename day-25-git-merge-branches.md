# Day 25: Git Merge Branches

**Category:** Git / Version Control

## Task

Create a new branch, add a file to it, commit and push the branch, then merge it back into `master` and push the merged result.

---

## Solution

### Step 1: Navigate to the repository and check existing branches

```bash
cd /usr/src/kodekloudrepos/beta
git branch
```

### Step 2: Create and switch to a new branch

```bash
git checkout -b xfusion
```

### Step 3: Add a new file

```bash
cp /tmp/index.html .
git add index.html
```

### Step 4: Commit the change

```bash
git commit -m 'index added'
```

### Step 5: Push the new branch to the remote

```bash
git push origin xfusion
```

### Step 6: Switch back to master

```bash
git checkout master
```

### Step 7: Merge the feature branch into master

```bash
git merge xfusion
```

### Step 8: Push the merged master

```bash
git push origin master
```

---

## Key Takeaways

- The command to list branches is `git branch` (singular) — `git branches` isn't a valid Git command and will just return `git: 'branches' is not a git command`.
- Pushing a brand-new local branch for the first time (`git push origin xfusion`) needs the branch to already exist as a ref locally, which `git checkout -b` provides — but note this push doesn't set up tracking automatically on older Git versions; if a plain `git push` later complains about no upstream, use `git push -u origin xfusion` once to link them.
- `git merge xfusion` while on `master` performs a **fast-forward** merge if `master` hasn't moved since `xfusion` branched off — no merge commit is created in that case. If `master` *has* moved in the meantime, Git creates an actual merge commit (or flags conflicts to resolve first).
- Pushing the feature branch (`xfusion`) *before* merging isn't strictly required for the merge to work locally — but it's good practice, since it means the work exists on the remote even if the local merge/push step fails or is interrupted.
- Always confirm the merge succeeded cleanly (`git status`, `git log --oneline --graph`) before pushing `master` — pushing a merge with unresolved conflict markers still committed is a common and disruptive mistake.

---

**Stack:** `Git` `Linux` `Version Control`
