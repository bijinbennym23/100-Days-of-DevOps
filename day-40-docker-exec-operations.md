# Day 40: Docker EXEC Operations

**Category:** Docker / Containers

## Task

A Nautilus DevOps team member was configuring services in a container named `kkloud` on App Server 3 in the Stratos Datacenter, but he's on PTO and the work has to be finished. Remaining work:

1. Install `apache2` in the `kkloud` container using `apt`.
2. Configure Apache to listen on port `8089` instead of the default HTTP port. It must not be bound to a specific IP or hostname, so it should respond on `localhost`, `127.0.0.1`, the container IP and so on.
3. Make sure the Apache service is up and running inside the container, and leave the container running.

---

## Solution

### Step 1: Connect to App Server 3 and open a shell in the container

```bash
ssh banner@stapp03
docker exec -it kkloud bash
```

`docker exec -it` starts an interactive shell inside the already-running container. The commands below all run inside that shell.

### Step 2: Install Apache

```bash
apt update
apt install apache2 -y
```

`apt update` refreshes the package index first. Minimal container images often ship without one, so the install can fail without it.

### Step 3: Install an editor (optional)

```bash
apt install vim -y
```

Container images usually don't include an editor. Alternatively, skip this and use `sed` in the next step.

### Step 4: Change the listening port

```bash
vim /etc/apache2/ports.conf
```

Change:

```text
Listen 80
```

to:

```text
Listen 8089
```

Use a bare port number with no IP address in front of it. `Listen 8089` binds to all interfaces, which satisfies the "don't bind to a specific IP or hostname" requirement. Writing `Listen 127.0.0.1:8089` would restrict it to localhost only.

The same change without an editor:

```bash
sed -i 's/^Listen 80$/Listen 8089/' /etc/apache2/ports.conf
```

### Step 5: Update the default virtual host to match (recommended)

```bash
sed -i 's/<VirtualHost \*:80>/<VirtualHost *:8089>/' /etc/apache2/sites-available/000-default.conf
```

The default site is declared for port 80. Updating it keeps the virtual host and the `Listen` directive consistent.

### Step 6: Restart Apache and check it

```bash
service apache2 restart
service apache2 status
```

The status should report that Apache is running.

### Step 7: Confirm it's listening on 8089

```bash
apt install curl -y
curl http://localhost:8089
```

A response with the default Apache page (or its HTML) confirms the port change worked. Then leave the shell with `exit`. The container keeps running, because exiting a `docker exec` session doesn't stop the container.

---

## Key Takeaways

- **`docker exec` runs a command inside a running container.** With `-it` and `bash` you get an interactive shell. When you exit, only that shell ends, and the container's main process keeps running.
- **Containers have no init system by default.** There's usually no systemd inside, so `systemctl` doesn't work. Debian/Ubuntu images use the `service` command (or calling `apachectl` / `apache2ctl` directly) instead.
- **`Listen 8089` versus `Listen 127.0.0.1:8089`.** A bare port listens on every interface, and an IP:port form restricts it to one address. The task's wording about not binding to a specific IP is exactly this distinction.
- **Apache in a container doesn't survive a container restart on its own.** The Apache process was started manually through `exec`, and changes made inside a running container live only in that container's writable layer. To make it permanent, bake the setup into a Dockerfile (or commit the container, as in Day 39).
- **`apt update` before `apt install`.** Slim images ship with empty package lists, so skipping the update is a common cause of "Unable to locate package" errors.
- **Check from inside the container.** The port is only reachable from the host if it's published (`-p`) when the container is created. The `curl` test inside the container verifies Apache itself, independent of any port mapping.

---

**Stack:** `Docker` `Apache` `Containers` `Linux`
