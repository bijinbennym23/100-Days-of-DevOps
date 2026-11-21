# Day 45: Resolve Dockerfile Issues

**Category:** Docker / Troubleshooting

## Task

The Nautilus DevOps team is building new images to the development team's requirements. A colleague is writing a `Dockerfile` on App Server 2 in the Stratos DC, but `docker build` fails with errors. Fix it so the image builds:

1. The `Dockerfile` is in `/opt/docker` on App Server 2.
2. Fix the issues so the image builds.
3. Don't change the base image, any other valid configuration in the Dockerfile, or any data it uses (for example `index.html`).

---

## Solution

### Step 1: Connect and look at the file

```bash
ssh steve@stapp02
cd /opt/docker/
cat Dockerfile
ls -R .
```

`ls -R` shows the build context: the Dockerfile, the `certs/` directory (`server.crt`, `server.key`) and the `html/` directory (`index.html`). Every `COPY` source has to exist inside this context.

### Step 2: Try the build and read the error

```bash
docker build -t test-img .
```

The failing step is named in the build output. Fix that line, rebuild, and repeat until it passes.

### Step 3: Edit the Dockerfile

```bash
vi Dockerfile
```

Corrected file:

```dockerfile
FROM httpd:2.4.43

RUN sed -i "s/Listen 80/Listen 8080/g" /usr/local/apache2/conf/httpd.conf
RUN sed -i '/LoadModule\ ssl_module modules\/mod_ssl.so/s/^#//g' conf/httpd.conf
RUN sed -i '/LoadModule\ socache_shmcb_module modules\/mod_socache_shmcb.so/s/^#//g' conf/httpd.conf
RUN sed -i '/Include\ conf\/extra\/httpd-ssl.conf/s/^#//g' conf/httpd.conf

COPY certs/server.crt /usr/local/apache2/conf/server.crt
COPY certs/server.key /usr/local/apache2/conf/server.key
COPY html/index.html /usr/local/apache2/htdocs/
```

What this does:

- Keeps the base image `httpd:2.4.43`.
- Changes Apache's listening port from `80` to `8080`.
- Uncomments the three lines that enable SSL: `mod_ssl`, `mod_socache_shmcb`, and the `httpd-ssl.conf` include.
- Copies the certificate, key and `index.html` into the paths Apache expects.

### Step 4: Rebuild

```bash
docker build -t test-img .
docker images
```

The build should finish without errors, and `test-img` should be listed.

### Step 5: Run it and check

```bash
docker run -d test-img
docker ps
```

`docker ps` should show the container as `Up`. If it exits right away, `docker logs <container-id>` gives the reason (a bad certificate path or a missing module are the usual causes).

---

## Key Takeaways

- **Read the failing step, not the whole log.** `docker build` prints each step and stops at the first one that fails. The error sits directly under that step, so fix that line, rebuild, and repeat.
- **`COPY` sources must be inside the build context.** The path is relative to the directory you pass to `docker build` (the `.`), not to the container or the host root. A wrong folder name, wrong file name or a case mismatch fails with "not found".
- **Relative paths in `RUN` depend on `WORKDIR`.** The official `httpd` image sets its working directory to `/usr/local/apache2`, so `conf/httpd.conf` resolves correctly. In an image with a different working directory the same relative path would fail, and an absolute path is the safer habit.
- **`sed` needs the pattern to match the file.** The module lines in `httpd.conf` begin with `#` when disabled, so the `s/^#//` substitution removes the comment character. If the text inside the `/.../` address doesn't match the real line exactly (including spaces and slashes), nothing changes, and Apache later fails to start because the SSL config is missing its modules.
- **Enabling SSL takes three things together:** the `ssl_module` and `socache_shmcb_module` modules loaded, the `httpd-ssl.conf` file included, and the certificate and key placed where that file expects them (`conf/server.crt` and `conf/server.key`).
- **A successful build doesn't prove the container works.** Run it and check `docker ps`. Apache can exit immediately on a bad config, and `docker logs` or `docker run ... httpd -t` shows the config error.
- **Respect "don't change the rest".** Fix only what is broken: leave the base image, the valid directives and the data files (`index.html`, certificates) as they were.

---

**Stack:** `Docker` `Dockerfile` `Apache httpd` `SSL/TLS` `Troubleshooting`
