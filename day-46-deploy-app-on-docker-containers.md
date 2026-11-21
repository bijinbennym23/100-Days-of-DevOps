# Day 46: Deploy an App on Docker Containers

**Category:** Docker / Docker Compose

## Task

The Nautilus application development team finished an app they want to deploy on a containerized platform. The team wants to test the deployment on one app server before going live, as a complete stack defined in a Docker Compose file.

On App Server 3 in the Stratos Datacenter, create `/opt/sysops/docker-compose.yml` (exact name) with two services.

**Web service**

1. Container name `php_blog`.
2. Image `php` with any `apache` tag.
3. Map container port `80` to host port `8088`.
4. Map the container's `/var/www/html` to the host's `/var/www/html`.

**DB service**

1. Container name `mysql_blog`.
2. Image `mariadb` with any tag (preferably `latest`).
3. Map container port `3306` to host port `3306`.
4. Map the container's `/var/lib/mysql` to the host's `/var/lib/mysql`.
5. Set `MYSQL_DATABASE=database_blog` and use a custom non-root user with a complex password.

After starting the stack, `curl <server-ip or hostname>:8088/` should reach the app.

---

## Solution

### Step 1: Connect to App Server 3

```bash
ssh banner@stapp03
cd /opt/sysops/
```

### Step 2: Create the Compose file

```bash
sudo vi docker-compose.yml
```

Contents:

```yaml
services:
  web:
    image: php:apache
    container_name: php_blog
    ports:
      - "8088:80"
    volumes:
      - "/var/www/html:/var/www/html"

  db:
    image: mariadb:latest
    container_name: mysql_blog
    ports:
      - "3306:3306"
    volumes:
      - "/var/lib/mysql:/var/lib/mysql"
    environment:
      MYSQL_DATABASE: database_blog
      MYSQL_USER: <db-user>
      MYSQL_PASSWORD: <db-password>
      MYSQL_ROOT_PASSWORD: <root-password>
```

The first draft had `version: '3.8'` at the top. Compose ignores that key, so it's left out here. The user and password values are placeholders: pick your own non-root user and complex passwords. Real credentials don't belong in a public repo, and in a real setup they would come from an `.env` file or a secrets store.

The `MYSQL_ROOT_PASSWORD` line is there because the MariaDB image refuses to start unless a root password option is set.

### Step 3: Start the stack

First attempt:

```bash
docker-compose up
```

This failed because the hyphenated `docker-compose` (Compose V1) wasn't installed. The standalone V1 binary was downloaded as a workaround:

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

Running it then failed with a missing shared library:

```text
Error loading Python lib '/tmp/_MEIXZe596/libpython3.7m.so.1.0': dlopen: libcrypt.so.1: cannot open shared object file: No such file or directory
```

The fix for that error was installing the compatibility library:

```bash
sudo yum install -y libxcrypt-compat
```

Next, the user needed permission to talk to the Docker daemon:

```bash
sudo usermod -aG docker banner
newgrp docker
```

Then the stack started:

```bash
docker-compose up -d
```

**Simpler route:** if `docker compose version` works on the server (Compose V2, see Days 35 and 44), skip the download and the library fix entirely:

```bash
docker compose -f /opt/sysops/docker-compose.yml up -d
```

### Step 4: Verify

```bash
docker ps
curl stapp03.stratos.xfusioncorp.com:8088/
```

`docker ps` should show both `php_blog` and `mysql_blog` as `Up`, and the `curl` call should return the app's response from the `php_blog` container.

---

## Key Takeaways

- **One Compose file, one stack.** Both services live in the same file, share a default network, and start together with a single `up -d`. Inside that network the web container can reach the database by its service name (`db`), not only through the published port.
- **Bind mounts tie a container to host paths.** `/var/www/html:/var/www/html` serves the host's files from Apache, and `/var/lib/mysql:/var/lib/mysql` keeps the database files on the host so they survive the container being removed. The host paths must exist and be writable by the container's user.
- **MariaDB needs a root password option.** Set `MYSQL_ROOT_PASSWORD` (or `MYSQL_ALLOW_EMPTY_PASSWORD` / `MYSQL_RANDOM_ROOT_PASSWORD`), or the container exits at start. `MYSQL_DATABASE`, `MYSQL_USER` and `MYSQL_PASSWORD` only take effect on first initialisation, when the data directory is empty.
- **`container_name` must match the task exactly** (`php_blog`, `mysql_blog`). It also stops those services from being scaled to more than one instance.
- **The `permission denied` on the Docker socket means "not in the `docker` group".** `usermod -aG docker <user>` adds the user, and `newgrp docker` (or logging in again) makes the new group active in the current session.
- **Prefer the Compose V2 plugin over a downloaded V1 binary.** The V1 binary is an old PyInstaller-packaged Python app, which is why it needed `libcrypt.so.1`. V1 has been retired, and `docker compose` avoids both the download and the library problem.
- **Keep secrets out of the repo.** Passwords written into a Compose file get committed with it. An `.env` file listed in `.gitignore`, referenced as `${DB_PASSWORD}`, is the usual fix.
- **Publishing `3306` exposes the database on the host.** Fine for a lab test, but in production the DB port is usually left unpublished so only the web container can reach it.

---

**Stack:** `Docker` `Docker Compose` `PHP` `Apache` `MariaDB` `Containers`
