# Day 24: Git Create Branches

**Category:** Git / Version Control

## Task

Navigate to an existing repository, resolve a "dubious ownership" error if one comes up, switch to the base branch, and create a new working branch from it.

---

## Solution

### Step 1: Navigate to the repository

```bash
cd /usr/src/kodekloudrepos/apps
git status
```

### Step 2: Resolve "dubious ownership" if it appears

```text
fatal: detected dubious ownership in repository at '/usr/src/kodekloudrepos/apps'
To add an exception for this directory, call:

        git config --global --add safe.directory /usr/src/kodekloudrepos/apps
```

```bash
git config --global --add safe.directory /usr/src/kodekloudrepos/apps
```

### Step 3: Switch to the base branch

```bash
git checkout master
```

### Step 4: Create and switch to a new branch

```bash
git checkout -b xfusioncorp_apps
```

### Step 5: Verify the branch was created

```bash
git branch
```

Expected output: `xfusioncorp_apps` listed with an asterisk (`*`) marking it as the currently checked-out branch.

---

## Key Takeaways

- The "dubious ownership" error is a Git security feature (added to guard against a class of attacks where a repo directory is owned by a different user than the one running Git) — it triggers whenever the repo's directory owner doesn't match the current user, which is common when a repo was cloned by `root` or a service account but is later accessed as a different user.
- `git config --global --add safe.directory <path>` explicitly allows exactly that one path — it's the targeted fix; a broader (and riskier) alternative some guides suggest is `git config --global --add safe.directory '*'`, which trusts every repo directory regardless of ownership and isn't recommended outside of tightly controlled environments.
- `git checkout -b <name>` is shorthand for two operations: create a new branch, then switch to it — equivalent to `git branch <name>` followed by `git checkout <name>`.
- Always branch from the correct base (`master` here) explicitly rather than assuming you're already on it — `git checkout master` before `-b` ensures the new branch starts from the intended point in history, not wherever the previous checkout happened to leave you.
- `git branch` (no arguments) lists local branches only — it won't show remote branches unless run with `-r` or `-a`, which matters if you're trying to confirm whether a branch already exists somewhere before creating a duplicate.

---

**Stack:** `Git` `Linux` `Version Control`
