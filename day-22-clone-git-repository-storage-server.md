# Day 22: Clone Git Repository on Storage Server

**Category:** Git / Version Control

## Task

Clone an existing bare repository on the storage server into a working directory, so it can be used and modified like a normal local repo.

---

## Solution

### Step 1: Connect to the storage server

```bash
ssh natasha@ststor01
```

### Step 2: Navigate to the target directory

```bash
cd /usr/src/kodekloudrepos
```

### Step 3: Clone the bare repository

```bash
git clone /opt/official.git
```

Since the source path is a local filesystem path rather than a URL, Git clones it directly from disk without going over SSH/HTTP(S) — no network transport involved, just a local copy with full history and a proper working tree, unlike the bare source repo itself.

### Step 4: Verify the clone

```bash
ls -la
```

Expected: an `official/` directory containing a working tree plus a `.git/` subdirectory (unlike the bare repo from Day 21, this one has actual checked-out files).

```bash
cd official
git status
git log --oneline
```

---

## Key Takeaways

- Cloning from a local path (`/opt/official.git`) versus a remote URL (`ssh://` or `https://`) uses the same `git clone` command — Git detects the source type automatically from the path/URL format, no extra flags needed.
- The result of `git clone` on a bare repo is a **non-bare** repo — it always produces a working directory with checked-out files and a `.git/` folder, regardless of whether the source was bare or not.
- Running this clone directly *on* the storage server (rather than from a separate developer machine) is a common pattern when the storage server itself needs a working copy — for deployment scripts, build processes, or serving files directly from that checkout.
- `git clone /opt/official.git` (no destination argument) creates a directory named after the source, minus `.git` — here, `official/`. Pass a second argument to `git clone` if a different local directory name is needed.
- Always confirm the clone succeeded with `git status` and `git log` rather than just checking the directory exists — a shallow or interrupted clone can leave a directory present but with incomplete history.

---

**Stack:** `Git` `Linux` `Version Control`
