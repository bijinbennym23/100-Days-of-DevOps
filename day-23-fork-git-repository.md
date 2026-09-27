# Day 23: Fork a Git Repository

**Category:** Git / Gitea

## Task

Log into a self-hosted Gitea instance, locate a repository owned by another user, and fork it under your own account.

---

## Solution

### Step 1: Access the Gitea UI

Click the **Gitea** button on the top bar to open the Gitea web interface.

### Step 2: Log in

```
Username: jon
Password: Jon_pass123
```

### Step 3: Locate the target repository

Navigate to (or search for) `sarah/story-blog` — the repository owned by user `sarah`.

### Step 4: Fork it

Click the **Fork** button on the repository page, and confirm forking it under the `jon` account.

### Step 5: Verify the fork

Navigate to `jon/story-blog` and confirm it now appears under jon's own repositories, with a "forked from sarah/story-blog" indicator on the repo page.

---

## Key Takeaways

- A **fork** creates a full server-side copy of the repository under your own account, distinct from a local `git clone` — a fork lives on the Git hosting platform (Gitea, GitHub, GitLab, etc.) itself, while a clone is a copy on your local machine. The two are often used together: fork on the platform, then clone your fork locally to work on it.
- Forking preserves the link back to the original (`sarah/story-blog`), which is what enables opening a pull/merge request from the fork back to the upstream repo later — a plain clone has no such relationship.
- Self-hosted Gitea instances behave the same way as GitHub/GitLab for this workflow (fork → clone your fork → branch → commit → PR back to upstream) — the underlying Git mechanics don't change based on which platform is hosting the remote.
- Forking under a specific account (here, `jon`) requires being logged in as that account first — Gitea (like GitHub) won't offer the option to fork into an account you're not authenticated as.

---

**Stack:** `Git` `Gitea` `Version Control`
