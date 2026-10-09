# Day 29: Manage Git Pull Requests

**Category:** Git / Gitea / Code Review

## Task

Direct pushes to `master` aren't allowed, because that branch should only hold reviewed and approved work. Max has already pushed his story to the `story/fox-and-grapes` branch on a Gitea remote. Get it into `master` the proper way: open a pull request, assign a reviewer, and have the reviewer approve and merge it.

---

## Solution

### Step 1: Connect to the storage server as max

```bash
ssh max@ststor01
```

### Step 2: Inspect the cloned repository

```bash
ls
cd story-blog/
git log
```

The clone already sits in Max's home directory. `git log` should show Sarah's earlier story and its history, so check the author info and commit messages before opening the PR.

### Step 3: Open the Gitea UI and log in as max

Use the **Gitea UI** button in the top bar and sign in with Max's credentials (provided by the task environment).

### Step 4: Create the pull request

In the `story-blog` repository, create a new pull request with these settings:

- **Title:** `Added fox-and-grapes story`
- **Source branch (pull from):** `story/fox-and-grapes`
- **Target branch (merge into):** `master`

### Step 5: Assign a reviewer

Open the new PR, click **Reviewers** in the right-hand sidebar, and add `tom`.

### Step 6: Switch users

Log out of Gitea and log back in as `tom`.

### Step 7: Review, approve, and merge

Open the PR titled `Added fox-and-grapes story`, review the changes, approve it, and merge it into `master`.

### Step 8: Verify

Check that `master` now contains the story and that the PR shows as merged.

---

## Key Takeaways

- A **pull request** is a request to merge one branch into another, with a review step in between. Gitea, GitHub, and GitLab all use the same idea, and it's how teams keep `master` limited to reviewed work.
- The PR direction matters: the **source** is the branch with the new work (`story/fox-and-grapes`) and the **destination** is the protected branch (`master`). Swapping them would propose merging `master` into the feature branch instead.
- Separate roles are the point of the exercise: the author (`max`) opens the PR and the reviewer (`tom`) approves and merges it. The same person authoring and approving defeats the purpose of review.
- Running `git log` before opening the PR is a cheap sanity check that the local clone matches the remote and the commit authorship is what you expect.
- UI-only tasks leave no terminal trail, so take screenshots (or record the screen) of each step. Graders and future you both need evidence that the PR was created, reviewed, and merged.
- Credentials for lab environments belong in the task page, not in a public repo. This write-up leaves them out on purpose.

---

**Stack:** `Git` `Gitea` `Pull Requests` `Code Review`
