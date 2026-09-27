# Day 19: Install and Configure Web Application

**Category:** Linux / Web Servers

## Task

Install Apache, configure it to listen on a custom port, then deploy two separate static apps (`blog` and `apps`) under their own subdirectories in the document root, copying the content over from the jump host.

---

## Solution

### Step 1: Install and start Apache

```bash
sudo su -
dnf install httpd -y
systemctl start httpd
systemctl status httpd
```

### Step 2: Change Apache's listening port

```bash
vi /etc/httpd/conf/httpd.conf
```

Change:

```
Listen 80
```

to:

```
Listen 3002
```

Save, exit, and restart to apply:

```bash
systemctl restart httpd
```

### Step 3: Confirm Apache is listening on the new port

```bash
ss -tunlp | grep httpd
```

### Step 4: Drop back to the regular user

```bash
exit
```

### Step 5: Create staging directories

```bash
mkdir /tmp/{blog,apps}
```

### Step 6: Copy content from the jump host

From the jump host:

```bash
scp blog/index.html steve@stapp02:/tmp/blog
scp apps/index.html steve@stapp02:/tmp/apps
```

### Step 7: Move content into Apache's document root

Back on the target server:

```bash
sudo mkdir /var/www/html/{blog,apps}
sudo mv /tmp/blog/index.html /var/www/html/blog/
sudo mv /tmp/apps/index.html /var/www/html/apps/
```

### Step 8: Verify both apps are being served

```bash
curl http://localhost:3002/apps/
curl http://localhost:3002/blog/
```

---

## Key Takeaways

- `mkdir /tmp/{blog,apps}` uses bash **brace expansion** to create both directories in one command — equivalent to running `mkdir /tmp/blog /tmp/apps` separately, but shorter and less error-prone when the same prefix path repeats.
- Apache's document root (`/var/www/html/` by default on RHEL/CentOS) can serve multiple independent apps as sibling subdirectories — each one just needs to exist under the root with its own `index.html` or app files; no separate virtual host is required for this simple case.
- Always re-verify the actual listening port with `ss -tunlp | grep httpd` after changing `Listen` in `httpd.conf` — don't assume the config value is what's actually active until confirmed, especially after copy-pasting port numbers across multiple tasks (it's easy to test against the wrong port by habit).
- The staging step (copy to `/tmp` first, then `mv` into the doc root with `sudo`) is a common pattern when the deploying user doesn't have direct write access to `/var/www/html/` — content lands somewhere writable first, then gets moved into place with elevated privileges.
- `curl` against each subpath independently (`/apps/`, `/blog/`) confirms both are served correctly — testing only the root path wouldn't catch a case where one app deployed correctly and the other didn't.

---

**Stack:** `Linux` `Apache` `Web Servers` `SCP`
