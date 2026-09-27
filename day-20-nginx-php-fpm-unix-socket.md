# Day 20: Configure Nginx + PHP-FPM Using Unix Socket

**Category:** Linux / Web Stack

## Task

Install and configure Nginx on a custom port, install PHP-FPM 8.1, connect the two over a Unix socket (rather than a TCP port), and verify PHP files are served correctly.

---

## Solution

### Step 1: Install and configure Nginx on port 8095

```bash
sudo su -
sudo dnf install -y nginx
```

Edit the default server config:

```bash
sudo vi /etc/nginx/conf.d/default.conf
```

Change:

```nginx
listen 80;
root   /usr/share/nginx/html;
```

to:

```nginx
listen 8095;
root   /var/www/html;
```

> If `default.conf` doesn't exist, make the same change in the `server` block of `/etc/nginx/nginx.conf` instead.

Enable and start Nginx:

```bash
sudo systemctl enable --now nginx
```

### Step 2: Install PHP-FPM 8.1 via the Remi repo

```bash
sudo dnf install -y https://rpms.remirepo.net/enterprise/remi-release-9.rpm
sudo dnf module reset php -y
sudo dnf module enable php:remi-8.1 -y
sudo dnf install -y php-fpm php-cli php-common php-mysqlnd \
    php-gd php-xml php-mbstring php-curl php-zip php-bcmath
```

The Remi repo is needed because the distro's default PHP module stream usually doesn't include 8.1 — `dnf module reset` clears any previously enabled PHP stream before switching, avoiding a conflict when enabling `php:remi-8.1`.

### Step 3: Configure PHP-FPM to listen on a Unix socket

```bash
sudo mkdir -p /var/run/php-fpm
sudo vi /etc/php-fpm.d/www.conf
```

Change:

```
listen = 127.0.0.1:9000
```

to:

```
listen = /var/run/php-fpm/default.sock
```

And make sure the socket ownership matches Nginx's user:

```
listen.owner = nginx
listen.group = nginx
listen.mode = 0660
```

Restart and enable PHP-FPM:

```bash
sudo systemctl restart php-fpm
sudo systemctl enable php-fpm
```

### Step 4: Point Nginx at the PHP-FPM socket

```bash
sudo vi /etc/nginx/conf.d/default.conf
```

Add/modify the PHP location block:

```nginx
location ~ \.php$ {
    root   /var/www/html;
    fastcgi_pass unix:/var/run/php-fpm/default.sock;
    fastcgi_index index.php;
    include fastcgi_params;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
}
```

Restart Nginx:

```bash
sudo systemctl restart nginx
```

### Step 5: Test from the jump host

```bash
curl http://stapp03:8095/index.php
curl http://stapp03:8095/info.php
```

Both should return PHP-rendered output.

---

## Key Takeaways

- A **Unix socket** (`unix:/var/run/php-fpm/default.sock`) skips the TCP/IP stack entirely for local inter-process communication — generally slightly faster and more secure than `127.0.0.1:9000` since it's filesystem-permission-gated rather than network-port-gated, but it only works when both processes run on the **same host**.
- `listen.owner`, `listen.group`, and `listen.mode` on the PHP-FPM pool config matter as much as the socket path itself — if Nginx's user (`nginx`) doesn't have permission to read/write the socket file, requests fail with a 502 Bad Gateway even though both services report as "running."
- `dnf module reset php` before `dnf module enable php:remi-8.1` avoids a "conflicting module" error — DNF module streams are exclusive, so switching versions requires clearing the prior stream selection first.
- `fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;` is what tells PHP-FPM which actual file to execute on disk — get the `root` directive wrong or mismatched between the `location` block and the top-level `server` block, and PHP-FPM will report "No input file specified" even though Nginx is otherwise routing correctly.
- Testing both `index.php` and a second file (`info.php`) confirms PHP processing works generally, not just for one specific script — useful for ruling out a fluke pass/fail on a single file.

---

**Stack:** `Linux` `Nginx` `PHP-FPM` `Unix Socket` `Web Stack`
