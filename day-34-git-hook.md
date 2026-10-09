# Day 34: Git Hook

**Category:** Git / Automation

## Task

The Nautilus application development team works with a bare repository `/opt/media.git`, cloned under `/usr/src/kodekloudrepos` on the storage server in the Stratos DC. They want a hook on this repository.

Requirements:

1. Merge the `feature` branch into `master`, but **before pushing**, set up the hook below.
2. Create a `post-update` hook so that any push to `master` creates a release tag named `release-YYYY-MM-DD`, where the date is the current date (for example, on 20 June 2023 the tag is `release-2023-06-20`).
3. Test the hook at least once and create a release tag for today's release.
4. Push the changes.
5. Do it as the `natasha` user, and don't alter the repository's or existing directories' permissions.

---

## Solution

### Step 1: Connect and merge feature into master

```bash
ssh natasha@ststor01
cd /usr/src/kodekloudrepos/media/
sudo git checkout master
sudo git merge feature
```

The merge happens locally in the clone. Nothing reaches the bare repo until the push in Step 5.

### Step 2: Create the post-update hook in the bare repository

```bash
cd /opt/media.git/hooks/
sudo vi post-update
```

Contents:

```sh
#!/bin/sh

# This hook will be executed after any push to the repository.
# It creates a release tag named after today's date.

DATE=$(date +%Y-%m-%d)
TAG_NAME="release-$DATE"

# Check if the tag already exists to avoid errors
if ! git tag -l | grep -q "$TAG_NAME"; then
  git tag "$TAG_NAME"
  echo "Created tag: $TAG_NAME"
else
  echo "Tag $TAG_NAME already exists. Skipping..."
fi
```

### Step 3: Make the hook executable and owned by natasha

```bash
sudo chmod +x post-update
sudo chown natasha:natasha post-update
```

Git only runs a hook if the file is executable. The `chown` lets `natasha` run it without touching the rest of the repository's permissions.

### Step 4: Go back to the clone

```bash
cd /usr/src/kodekloudrepos/media
```

### Step 5: Push to trigger the hook

```bash
sudo git push origin master
```

The push output includes the hook's message, for example `remote: Created tag: release-<today>`.

### Step 6: Verify the tag exists on the remote

```bash
sudo git ls-remote --tags origin
```

Expected: a `refs/tags/release-<today's date>` line.

---

## Key Takeaways

- **Hooks live in the bare repository.** Server-side hooks belong in `/opt/media.git/hooks/`, not in the clone's `.git/hooks/`. A hook in the clone only fires for local actions in that clone.
- **`post-update` runs after a push has been accepted.** It can't reject or change the push, which makes it a good fit for follow-up actions such as tagging or notifications. To block a push, use `pre-receive` or `update` instead.
- **The file must be executable and have a shebang.** Git silently skips a hook that isn't executable, so `chmod +x` is part of the setup, not an extra.
- **The script above tags after any push, not just pushes to `master`.** The comment in the original script says "master only", but nothing checks the branch. `post-update` receives the pushed ref names as arguments, so a stricter version would test for `refs/heads/master` first:

  ```sh
  for ref in "$@"; do
    [ "$ref" = "refs/heads/master" ] && git tag "release-$(date +%Y-%m-%d)"
  done
  ```

- **Tags get the date of the push, not the commit.** `date` runs on the server at push time, so two pushes on the same day would try to create the same tag. The existence check in the script prevents an error but also means a second push that day doesn't get a new tag.
- `git ls-remote --tags origin` is a quick way to confirm the hook actually ran on the server side.

---

**Stack:** `Git` `Git Hooks` `Linux` `Automation`
