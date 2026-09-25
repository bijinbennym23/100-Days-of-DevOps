# Day 15: Setup SSL for Nginx

**Category:** Linux / Networking / Security

## Task

Install and configure Nginx, deploy a self-signed SSL certificate and key, enable HTTPS on the server block, serve a simple `index.html`, and verify the setup with `curl`.

---

## Solution

### Step 1: Install Nginx

```bash
yum install nginx -y
systemctl status nginx
```

### Step 2: Move the SSL certificate and key into place

```bash
mv /tmp/nautilus.crt /etc/pki/tls/certs
mv /tmp/nautilus.key /etc/pki/tls/private/
```

### Step 3: Update the Nginx config

```bash
vi /etc/nginx/nginx.conf
```

In the plain HTTP `server` block, set `server_name` to the server's IP:

```nginx
server {
    listen       80;
    listen       [::]:80;
    server_name  172.16.238.10;
    root         /usr/share/nginx/html;
    ...
}
```

In the TLS `server` block (usually commented out by default), uncomment it and set the `server_name`, certificate, and key paths:

```nginx
server {
    listen       443 ssl http2;
    listen       [::]:443 ssl http2;
    server_name  172.16.238.10;
    root         /usr/share/nginx/html;

    ssl_certificate "/etc/pki/tls/certs/nautilus.crt";
    ssl_certificate_key "/etc/pki/tls/private/nautilus.key";
    ssl_session_cache shared:SSL:1m;
    ssl_session_timeout  10m;
    ssl_ciphers PROFILE=SYSTEM;
    ssl_prefer_server_ciphers on;

    # Load configuration files for the default server block.
    include /etc/nginx/default.d/*.conf;

    error_page 404 /404.html;
    location = /40x.html {
    }

    error_page 500 502 503 504 /50x.html;
    location = /50x.html {
    }
}
```

### Step 4: Validate the config and start the service

```bash
nginx -t
systemctl restart nginx
systemctl status nginx
```

Expected `nginx -t` output:

```text
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

### Step 5: Create the index page

```bash
cd /usr/share/nginx/html
rm -f index.html
vi index.html
```

Contents:

```text
Welcome!
```

### Step 6: Test from the jump host

```bash
curl -Ik https://stapp01
```

Expected output:

```text
HTTP/2 200
server: nginx/1.20.1
date: Wed, 10 Sep 2025 12:53:21 GMT
content-type: text/html
content-length: 9
last-modified: Wed, 10 Sep 2025 12:52:11 GMT
etag: "68c1747b-9"
accept-ranges: bytes
```

---

## Key Takeaways

- `nginx -t` validates syntax **without** reloading or restarting the service — always run it before `restart`/`reload` so a bad config doesn't take down a service that was previously working.
- The HTTP (`:80`) and HTTPS (`:443`) blocks in `nginx.conf` are independent `server {}` blocks — both need `server_name` set correctly, and only the TLS block needs the `ssl_certificate` / `ssl_certificate_key` directives.
- `curl -Ik` combines `-I` (headers only, no body) with `-k` (skip certificate verification) — the `-k` flag is what lets `curl` connect successfully against a **self-signed** cert that isn't from a trusted CA; against a real CA-signed cert, `-k` wouldn't be necessary.
- Certificate and key file locations (`/etc/pki/tls/certs/`, `/etc/pki/tls/private/`) follow the RHEL/CentOS convention — Debian/Ubuntu systems typically use `/etc/ssl/certs/` and `/etc/ssl/private/` instead.
- `include /etc/nginx/default.d/*.conf;` inside the server block picks up any distro-provided drop-in config snippets — removing it can silently change default behavior that other tooling expects.

---

**Stack:** `Linux` `Nginx` `SSL/TLS` `Networking` `Security`
