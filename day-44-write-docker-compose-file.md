# Day 44: Write a Docker Compose File

**Category:** Docker / Docker Compose

## Task

The Nautilus application development team shared static website content that must be hosted on an `httpd` web server in a containerised setup. On App Server 2 in the Stratos DC:

1. Create a container named `httpd` using a Docker Compose file at `/opt/docker/docker-compose.yml` (use this exact file name).
2. Use the `httpd` image (preferably the `latest` tag) and name the container `httpd`. The service name can be anything.
3. Map container port `80` to host port `8087`.
4. Map the container's `/usr/local/apache2/htdocs` to the host's `/opt/dba`, which already exists. Don't modify any data in these locations.

---

## Solution

### Step 1: Connect to App Server 2

```bash
ssh steve@stapp02
sudo su
cd /opt/docker
```

### Step 2: Create the Compose file

```bash
vi /opt/docker/docker-compose.yml
```

Contents:

```yaml
services:
  httpd:
    container_name: httpd
    image: httpd:latest
    ports:
      - "8087:80"
    volumes:
      - /opt/dba:/usr/local/apache2/htdocs
```

The first draft used `version: '3'` at the top. Compose V2 ignores that key and prints a warning that it's obsolete, so it's left out here. The file works either way.

### Step 3: Start the container

The first attempt used the old standalone command:

```bash
docker-compose -f /opt/docker/docker-compose.yml up -d
```

```text
bash: docker-compose: command not found
```

Check which Compose is installed:

```bash
docker compose version
```

The server runs **Compose V2**, which is a Docker CLI plugin invoked with a space (`docker compose`) rather than a hyphen. Use:

```bash
docker compose -f /opt/docker/docker-compose.yml up -d
```

### Step 4: Verify

```bash
docker ps
```

Expected: a container named `httpd`, image `httpd:latest`, with PORTS showing `0.0.0.0:8087->80/tcp`.

```bash
curl http://localhost:8087
```

This should return the content served from `/opt/dba`.

---

## Key Takeaways

- **`docker-compose` (hyphen) vs `docker compose` (space).** The hyphenated binary is Compose V1, a separate Python tool that has been retired. Compose V2 ships as a plugin to the Docker CLI. "command not found" for `docker-compose` usually just means V2 is installed, so try the space form (see Day 35, where the `docker-compose-plugin` package is installed).
- **`version:` is obsolete.** Current Compose follows the Compose Specification and ignores the top-level `version` key. Leaving it in only produces a warning.
- **`container_name` fixes the container's name.** Without it Compose names containers `<project>-<service>-<number>`. The task requires the exact name `httpd`. A side effect is that you can't scale that service past one instance, since names must be unique.
- **Quote the port mapping.** `"8087:80"` is safer than a bare `8087:80`. YAML can read numbers like `22:22` as a base-60 value, so quoting avoids surprises. The format is `host:container`.
- **A bind mount shows the host directory inside the container.** `/opt/dba:/usr/local/apache2/htdocs` replaces whatever the image has at that path with the host's `/opt/dba`. Apache serves those files directly, and changes on the host appear immediately. Mounting over `htdocs` hides the image's default `index.html`, which is the intended behaviour here.
- **Don't modify the mounted data.** The task explicitly protects `/opt/dba`. Avoid `docker compose down -v` style cleanups and avoid writing into the folder.
- **`-f` selects the Compose file.** It lets you run the command from any directory. Without `-f`, Compose looks for `compose.yaml` or `docker-compose.yml` in the current directory.
- **`up -d` is declarative.** It creates what's missing and leaves matching containers alone, so running it again is safe.

---

**Stack:** `Docker` `Docker Compose` `Apache httpd` `Volumes` `Containers`
