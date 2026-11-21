# Day 36: Deploy Nginx Container on Application Server

**Category:** Docker / Containers

## Task

The Nautilus DevOps team is running application deployment tests on selected application servers. They need an Nginx container on App Server 2:

1. Create a container named `nginx_2` using the `nginx` image with the `alpine` tag.
2. Make sure the container is in a `running` state.

---

## Solution

### Step 1: Connect to App Server 2

```bash
ssh steve@stapp02
```

### Step 2: Pull the image

```bash
docker pull nginx:alpine
```

### Step 3: Run the container in the background with the required name

```bash
docker run -d --name nginx_2 nginx:alpine
```

- `-d` runs the container detached, in the background.
- `--name nginx_2` sets the exact container name the task asks for.
- `nginx:alpine` is the image and tag: the Nginx image built on the small Alpine Linux base.

### Step 4: Verify it's running

```bash
docker ps
```

Expected: a row for `nginx_2`, image `nginx:alpine`, with a status like `Up X seconds`.

---

## Key Takeaways

- **The tag matters.** `nginx:alpine` is a much smaller image than the default `nginx` (Debian-based). If you leave off the tag, Docker uses `latest`, which isn't what the task asked for.
- **`-d` keeps the container running.** Without it, the container runs in the foreground and takes over your terminal. Closing it or pressing `Ctrl+C` stops the container. Nginx is designed to run as a long-lived foreground process, so in detached mode it simply stays up.
- **`docker pull` is optional but explicit.** `docker run` pulls the image automatically if it isn't present locally. Pulling first just separates "download the image" from "start the container", which makes failures easier to diagnose.
- **Container names must be unique.** Re-running the same `docker run --name nginx_2 ...` fails if a container with that name already exists, even a stopped one. Remove it with `docker rm nginx_2` (or `docker rm -f nginx_2` if it's running) before recreating it.
- **`docker ps` only lists running containers.** If `nginx_2` doesn't appear, check `docker ps -a` to see whether it exited, then `docker logs nginx_2` to find out why.
- No `-p` flag was used because the task only asks for a running container. To reach Nginx from outside the host, you'd publish a port, for example `-p 8080:80`.

---

**Stack:** `Docker` `Nginx` `Containers` `Linux`
