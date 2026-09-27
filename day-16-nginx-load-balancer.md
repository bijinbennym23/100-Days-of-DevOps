# Day 16: Install and Configure Nginx as an LBR

**Category:** Linux / Networking / Load Balancing

## Task

Traffic on a production website is growing and the app is being migrated to a high-availability stack across multiple app servers. The only piece left is the load balancer (LBR):

1. Install Nginx on the LBR server.
2. Configure load balancing in the `http` context, using all app servers — editing only `/etc/nginx/nginx.conf`.
3. Don't change the Apache port already configured on the app servers; confirm Apache is up and running on all of them.

Reference: [nginx.org - HTTP Load Balancing](https://nginx.org/en/docs/http/load_balancing.html)

---

## Solution

### Step 1: Install Nginx on the LBR server

```bash
ssh loki@stlb01
sudo su
dnf install nginx -y
systemctl restart nginx
systemctl status nginx
```

### Step 2: Confirm the port Apache is using on each app server

```bash
ssh tony@stapp01
sudo su
ss -tulpn | grep httpd
```

Expected output:

```text
tcp   LISTEN 0      511          0.0.0.0:5001       0.0.0.0:*
```

`netstat` isn't available on newer systems by default — `ss` is the modern equivalent, same flags (`-t` TCP, `-u` UDP, `-l` listening, `-p` process, `-n` numeric). Repeat this check on `stapp02` and `stapp03` to confirm they're all listening on the same port (`5001` here) — the upstream block in Step 3 assumes they match.

### Step 3: Configure the upstream and proxy_pass on the LBR

Back on `stlb01`:

```bash
vi /etc/nginx/nginx.conf
```

Inside the `http` block, define the upstream group:

```nginx
upstream appservers {
    server stapp01:5001;
    server stapp02:5001;
    server stapp03:5001;
}
```

Inside the relevant `server` block's `location /`, proxy to that upstream group:

```nginx
location / {
    proxy_pass http://appservers;
}
```

The name after `http://` in `proxy_pass` must exactly match the `upstream` block's name (`appservers` here).

### Step 4: Validate and reload

```bash
nginx -t
```

Expected output:

```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

```bash
systemctl restart nginx
```

### Step 5: Verify

Hit the LBR's address in a browser or via `curl` — requests should be distributed across `stapp01`, `stapp02`, and `stapp03` on port `5001`.

---

## Key Takeaways

- `upstream { ... }` defines a named pool of backend servers; `proxy_pass http://<upstream-name>;` is what actually routes traffic to that pool — the two are linked purely by matching names, so a typo in either breaks the config silently (it'll pass `nginx -t` if the syntax is valid, but won't route where you expect).
- The task explicitly requires editing **only** `nginx.conf` — no separate `conf.d` include files — and requires **not** touching Apache's existing port on the app servers. The LBR only needs to know what port Apache is already using, not change it.
- Always confirm the backend port independently on **every** app server before wiring up the upstream block — assuming they all match without checking is exactly the kind of assumption that produces hard-to-diagnose 502s later.
- `ss -tulpn` (or the legacy `netstat -tulpn`) is the reliable way to confirm what a service is actually listening on — don't trust a config file's stated port without verifying the running process matches it.
- `nginx -t` before `restart`/`reload` remains the standard safety check (same as Day 15) — validate before applying, every time.

---

**Stack:** `Linux` `Nginx` `Load Balancing` `Networking` `Apache`
