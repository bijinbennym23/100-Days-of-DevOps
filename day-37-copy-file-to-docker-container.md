# Day 37: Copy File to Docker Container

**Category:** Docker / Containers

## Task

The Nautilus DevOps team has confidential data on App Server 1 in the Stratos Datacenter, and a container named `ubuntu_latest` is running on that same server.

Copy the encrypted file `/tmp/nautilus.txt.gpg` from the Docker host into the `ubuntu_latest` container at `/home/`, and make sure the file is not modified during the copy.

---

## Solution

### Step 1: Connect to App Server 1

```bash
ssh tony@stapp01
```

### Step 2: Confirm the container is running

```bash
docker ps
```

Look for `ubuntu_latest` in the list. If it isn't there, `docker ps -a` shows whether it has stopped.

### Step 3: Copy the file into the container

```bash
docker cp /tmp/nautilus.txt.gpg ubuntu_latest:/home/
```

The format is `docker cp <host-source> <container>:<destination>`. The file is copied byte for byte, so the encrypted contents are untouched.

### Step 4: Verify the file is in the container

```bash
docker exec ubuntu_latest ls -l /home/
```

Expected: `nautilus.txt.gpg` listed in the output.

### Step 5: Confirm the file wasn't modified (optional)

```bash
sha256sum /tmp/nautilus.txt.gpg
docker exec ubuntu_latest sha256sum /home/nautilus.txt.gpg
```

Both checksums should match exactly.

---

## Key Takeaways

- **`docker cp` copies in both directions.** `docker cp <host-path> <container>:<path>` goes into a container, and `docker cp <container>:<path> <host-path>` pulls a file out. The container-side path is always written with the `container:` prefix.
- **It works on running and stopped containers.** The container doesn't need a shell or any special tools for `docker cp` to work, because the copy is done by the Docker daemon, not by a process inside the container.
- **"Not modified" is satisfied by a plain copy.** `docker cp` doesn't transform file contents, so an already-encrypted `.gpg` file arrives as-is. A checksum comparison on both sides is a quick way to prove it.
- **A trailing slash on the destination means "put it in this directory."** `ubuntu_latest:/home/` places the file inside `/home/` under its original name, while a full path like `ubuntu_latest:/home/other-name.gpg` would also rename it.
- **Copied files are owned by root inside the container by default**, regardless of who owns them on the host. That's fine for this task, but worth knowing if a non-root process in the container needs to read the file later.
- `docker exec ... ls` is the simplest check that the file landed where you intended. Without `-it`, the command runs non-interactively and just prints its output, which is all that's needed here.

---

**Stack:** `Docker` `Containers` `Linux` `Security`
