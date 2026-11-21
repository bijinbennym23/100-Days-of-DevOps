# Day 43: Docker Ports Mapping

**Category:** Docker / Networking

## Task

The Nautilus DevOps team plans to host an application on an Nginx-based container. One of the tickets asks for an Nginx container on Application Server 1 in the Stratos Datacenter:

1. Pull the `nginx:alpine-perl` image.
2. Create a container named `games` from that image.
3. Map host port `6400` to container port `80`, and keep the container running.

---

## Solution

### Step 1: Connect to App Server 1

```bash
ssh tony@stapp01
```

### Step 2: Pull the image

```bash
docker pull nginx:alpine-perl
```

### Step 3: Run the container with the port mapping

```bash
docker run -d --name games -p 6400:80 nginx:alpine-perl
```

- `-d` runs the container in the background, so it stays running.
- `--name games` sets the required container name.
- `-p 6400:80` maps **host** port `6400` to **container** port `80` (format `host:container`).
- `nginx:alpine-perl` is the Alpine-based Nginx image that includes the Perl module.

### Step 4: Verify the container and the mapping

```bash
docker ps
```

Expected: `games` with status `Up` and a PORTS column like `0.0.0.0:6400->80/tcp`.

### Step 5: Test that Nginx answers on the host port

```bash
curl http://localhost:6400
```

This should return the default Nginx welcome page.

---

## Key Takeaways

- **Port mapping order is `host:container`.** In `-p 6400:80`, traffic arriving at port `6400` on the host is forwarded to port `80` inside the container. Reversing the two is a very common mistake.
- **Containers are isolated by default.** Without `-p`, Nginx listens on port 80 inside the container, but nothing outside can reach it. Publishing the port is what makes the app reachable from the host and network.
- **`EXPOSE` doesn't publish ports.** It's metadata in the image. Only `-p` (or `-P`, which maps every exposed port to a random host port) actually opens a port on the host.
- **A host port can only be used once.** If something already listens on `6400`, `docker run` fails with an "address already in use" error. `ss -tulnp | grep 6400` shows what holds it.
- **The `alpine-perl` tag is a variant of the Nginx image.** It's built on Alpine Linux (small) and includes the `ngx_http_perl_module`. Using the exact tag the task names matters, since `nginx:latest` is a different, larger image.
- **Bind to a specific interface when needed.** `-p 127.0.0.1:6400:80` would make the port reachable only from the host itself, instead of every interface.
- Keeping a container running relies on `-d` plus a foreground main process. Nginx's official images start it with `daemon off;`, so the container stays up.

---

**Stack:** `Docker` `Nginx` `Port Mapping` `Containers` `Networking`
