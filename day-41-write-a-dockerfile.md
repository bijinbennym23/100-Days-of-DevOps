# Day 41: Write a Docker File

**Category:** Docker / Containers

## Task

The Nautilus application development team needs custom images for one of their projects. On App Server 2 in the Stratos DC, create a Dockerfile at `/opt/docker/Dockerfile` (with a capital `D`) that builds an image meeting these requirements:

1. Use `ubuntu:24.04` as the base image.
2. Install `apache2` and configure it to listen on port `8084`. Don't change any other Apache settings, such as the document root.

---

## Solution

### Step 1: Connect to App Server 2 and go to the target directory

```bash
ssh steve@stapp02
cd /opt/docker/
```

### Step 2: Create the Dockerfile

```bash
sudo vi /opt/docker/Dockerfile
```

Contents:

```dockerfile
# a) Use ubuntu:24.04 as the base image
FROM ubuntu:24.04

# Prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# b) Install apache2
RUN apt-get update && \
    apt-get install -y apache2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configure Apache to listen on port 8084
RUN sed -i 's/^Listen 80$/Listen 8084/' /etc/apache2/ports.conf && \
    sed -i 's/<VirtualHost \*:80>/<VirtualHost *:8084>/' /etc/apache2/sites-available/000-default.conf

# Document the port
EXPOSE 8084

# Run Apache in the foreground so the container keeps running
CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
```

Save and exit the editor (`Esc`, then `:wq!`).

### Step 3: Build the image

```bash
docker build -t custom-apache:latest .
```

The `.` is the build context, the directory that contains the Dockerfile.

### Step 4: Test the image (optional)

```bash
docker run -d --name test-apache -p 8084:8084 custom-apache:latest
docker ps
curl http://localhost:8084
```

`docker ps` should show `test-apache` as `Up`, and `curl` should return the default Apache page.

---

## Key Takeaways

- **The file name is case-sensitive.** `docker build` looks for a file called exactly `Dockerfile` in the build context. A file named `dockerfile` won't be found unless you point to it with `-f`.
- **Each `RUN` creates a layer.** Chaining `apt-get update`, `install`, `clean` and the cache removal in one `RUN` keeps the image smaller, because files deleted in a later layer still take up space in the earlier one.
- **Always run `apt-get update` in the same `RUN` as `apt-get install`.** If they're separate, Docker can cache a stale package index and the install fails later.
- **`DEBIAN_FRONTEND=noninteractive`** stops apt from waiting for input (for example a timezone prompt), which would hang the build. Setting it with `ENV` also applies to every later step and persists in the final image, so `ARG DEBIAN_FRONTEND=noninteractive` is the tidier choice when you don't want it at runtime.
- **Change the port in two places.** Apache needs `Listen 8084` in `ports.conf` **and** a matching `<VirtualHost *:8084>` in the default site. Updating only one leaves the default site unreachable.
- **`EXPOSE` is documentation, not publishing.** It records the intended port but doesn't open it. You still need `-p host:container` on `docker run`.
- **Run Apache in the foreground.** A container stops when its main process exits. `apache2ctl -D FOREGROUND` keeps Apache as the main process, while `service apache2 start` would return immediately and the container would exit.
- Anchoring the `sed` pattern (`^Listen 80$`) avoids accidentally matching other lines that begin with `Listen 80`.

---

**Stack:** `Docker` `Dockerfile` `Apache` `Ubuntu` `Containers`
