# Day 39: Create a Docker Image From Container

**Category:** Docker / Containers

## Task

A Nautilus developer was testing new changes inside a container and wants a backup of that work. The DevOps team has been asked to create a new image from the container.

On App Server 3, create an image `apps:nautilus` from the running container `ubuntu_latest`.

---

## Solution

### Step 1: Connect to App Server 3

```bash
ssh banner@stapp03
```

### Step 2: Confirm the container exists and is running

```bash
docker ps
```

Look for `ubuntu_latest` in the list.

### Step 3: Commit the container to a new image

```bash
docker commit ubuntu_latest apps:nautilus
```

The format is `docker commit <container> <repository>:<tag>`. Docker takes a snapshot of the container's current filesystem and saves it as a new image.

### Step 4: Verify the image was created

```bash
docker images
```

Expected: a row for `apps` with the tag `nautilus`.

---

## Key Takeaways

- **`docker commit` captures the container's current state.** Any files added, packages installed or config changed inside the container since it started become part of the new image, which is exactly what "keep a backup of his changes" asks for.
- **The container doesn't need to be stopped.** `docker commit` works on a running container. By default Docker pauses it briefly while taking the snapshot, so the filesystem stays consistent.
- **Data in volumes isn't included.** Only the container's own filesystem layer is committed. Anything stored in a mounted volume or bind mount stays outside the image.
- **`commit` is fine for backups, but a Dockerfile is better for reproducibility.** An image made by committing has no record of how it was built. For anything repeatable or shared, write the steps into a Dockerfile and use `docker build`.
- **The image gets its own name, independent of the container.** After committing, you can start new containers from it with `docker run apps:nautilus`, and the original container is left unchanged.
- **Useful flags:** `-m "message"` adds a commit message and `-a "author"` records an author, both visible later in `docker history apps:nautilus`.

---

**Stack:** `Docker` `Containers` `Linux`
