# Day 38: Pull Docker Image

**Category:** Docker / Containers

## Task

Nautilus project developers are starting tests on a new project and want to try containerized application features. On App Server 3 in the Stratos DC:

1. Pull the `busybox:musl` image.
2. Re-tag (create a new tag for) this image as `busybox:media`.

---

## Solution

### Step 1: Connect to App Server 3

```bash
ssh banner@stapp03
```

### Step 2: Pull the image

```bash
docker pull busybox:musl
```

### Step 3: Create the new tag

```bash
docker tag busybox:musl busybox:media
```

The format is `docker tag <source-image>:<tag> <target-image>:<new-tag>`.

### Step 4: Verify both tags exist

```bash
docker images
```

Expected: two rows for `busybox`, one tagged `musl` and one tagged `media`, both with the **same IMAGE ID**.

---

## Key Takeaways

- **Tagging doesn't copy anything.** `docker tag` just adds another name that points at the same image. That's why both rows in `docker images` show an identical image ID and no extra disk space is used.
- **A tag is a label, not a version lock.** Tags like `musl` or `latest` can be moved to point at a different image later, so the image ID (or digest) is the real identity of an image.
- **Re-tagging is how images are prepared for a registry.** To push to a private registry you'd tag with the registry path first, for example `docker tag busybox:musl registry.example.com/busybox:media`, then `docker push` it.
- **`busybox:musl` is the variant built on musl libc** rather than glibc. It's a very small image, which is why BusyBox is a common choice for quick container tests.
- **Removing a tag only removes that name.** `docker rmi busybox:media` deletes the `media` label, but the image data stays until every tag pointing at it is gone.
- Pulling with an explicit tag (`busybox:musl`) avoids silently getting `latest`, which is a different image.

---

**Stack:** `Docker` `Containers` `Linux`
