# Day 33: Resolve Git Merge Conflicts

**Category:** Git / Version Control

## Task

Sarah and Max have been writing stories and pushing them to a shared repository. Max added new changes but can't push them. Fix the problem and get his work onto the origin:

1. On the storage server, find the `story-blog` repository under `/home/max` and try to push to the origin.
2. Fix whatever blocks the push.
3. `story-index.txt` must list the titles of **all 4 stories**.
4. Fix the typo in the `The Lion and the Mooose` line: `Mooose` should be `Mouse`.

The Gitea web UI (top bar button) can be used to check the result. Because part of this task is UI-based, take screenshots or a screen recording in case the task needs review.

---

## Solution

### Step 1: Connect to the storage server as max

```bash
ssh max@ststor01
cd /home/max/story-blog
```

Login credentials come from the task page and are intentionally not recorded here.

### Step 2: Try to push (and see it fail)

```bash
git push origin master
```

The push is rejected because Sarah has pushed commits that Max's local `master` doesn't have yet (a non-fast-forward rejection).

### Step 3: Pull the remote changes

```bash
git pull
```

Both sides edited `story-index.txt`, so Git stops with a merge conflict and marks the file.

### Step 4: Resolve the conflict by hand

```bash
vi story-index.txt
```

The conflicting region looks like this:

```text
<<<<<<< HEAD
(Max's version of the lines)
=======
(Sarah's version of the lines)
>>>>>>> <commit>
```

Edit the file so that it:

- keeps the titles from both sides, giving **4 stories** in total,
- has `The Lion and the Mouse` spelled correctly,
- contains **no** `<<<<<<<`, `=======` or `>>>>>>>` marker lines.

### Step 5: Verify the file

```bash
cat story-index.txt
grep -n '<<<<<<<\|=======\|>>>>>>>' story-index.txt
```

The `grep` should print nothing. Count the titles to confirm there are four.

### Step 6: Commit the merge resolution

```bash
git add .
git commit -m "Fixed index titles and typo in The Lion and the Mouse story"
```

### Step 7: Push

```bash
git push origin master
```

### Step 8: Check in Gitea

Open the Gitea UI, log in with either user's credentials from the task page, and open `sarah/story-blog` on `master`. Confirm `story-index.txt` shows all 4 titles with the corrected spelling.

---

## Key Takeaways

- A rejected push (non-fast-forward) means the remote has commits you don't. The fix is to bring those in with `git pull` (or `git fetch` plus merge/rebase) first, then push again. Forcing the push would erase Sarah's work.
- `git pull` is a `fetch` followed by a `merge`. When both sides changed the same lines, Git can't pick a winner, so it stops and writes conflict markers into the file.
- Conflict markers have three parts: `<<<<<<<` starts your side, `=======` separates the two versions, and `>>>>>>>` ends the other side. Resolving means editing the file to the final intended content and **deleting all three marker lines**.
- Resolving a conflict is not just choosing one side. Here both sets of titles had to be kept so the index lists all four stories.
- After editing, `git add` marks the file as resolved, and `git commit` completes the merge. `git status` during a conflict shows which files are still "unmerged".
- Grepping for leftover markers before committing catches the classic mistake of committing a file that still contains `<<<<<<<`.
- Never commit lab or personal passwords into a public repo. The task page's credentials stay out of this write-up on purpose.

---

**Stack:** `Git` `Gitea` `Merge Conflicts` `Linux`
