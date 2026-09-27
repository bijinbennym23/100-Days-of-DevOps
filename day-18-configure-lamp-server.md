# Day 18: Configure LAMP Server

**Category:** Linux / Web Stack

## Task

Set up a LAMP (Linux, Apache, MySQL/MariaDB, PHP) stack: install PHP with common extensions, install and configure Apache on a custom port, install MariaDB, and create a database with a dedicated user.

---

## Solution

### Step 1: Install PHP and common extensions

```bash
yum install php php-opcache php-gd php-curl php-mysqlnd -y
```

### Step 2: Install and start Apache

```bash
yum install httpd -y
systemctl start httpd
systemctl status httpd
```

### Step 3: Start PHP-FPM

```bash
systemctl start php-fpm
systemctl status php-fpm
```

PHP-FPM (FastCGI Process Manager) is what actually executes PHP code and hands the result back to Apache — Apache alone doesn't know how to run `.php` files without it (or an equivalent `mod_php`).

### Step 4: Configure Apache to serve on a custom port

```bash
vi /etc/httpd/conf/httpd.conf
```

Change:

```
Listen 80
```

to:

```
Listen 6100
```

Save and exit, then restart Apache to apply:

```bash
systemctl restart httpd
```

### Step 5: Install MariaDB

```bash
dnf install mariadb mariadb-server -y
```

### Step 6: Enable and start MariaDB

```bash
systemctl enable mariadb
systemctl restart mariadb
systemctl status mariadb
```

### Step 7: Create a database and a dedicated user

```bash
sudo -u root mysql
```

```sql
CREATE DATABASE kodekloud_db6;
GRANT ALL PRIVILEGES ON kodekloud_db6.* TO 'kodekloud_pop'@'%' IDENTIFIED BY 'YchZHRcLkL';
```

### Step 8: Verify the user was created

```sql
SELECT user, host FROM mysql.user;
```

---

## Key Takeaways

- Changing `Listen 80` to `Listen 6100` in `httpd.conf` requires a **restart**, not just a config save — Apache only re-reads its listening ports on start/restart, not on a plain reload in all cases, so confirm with `systemctl status httpd` that it actually came back up on the new port.
- `GRANT ... IDENTIFIED BY` in a single statement both creates the user (if it doesn't exist) and grants privileges in one step — an older MySQL/MariaDB pattern that's since been deprecated in favor of separate `CREATE USER` + `GRANT` statements (as used explicitly in Day 17), though it's still commonly seen and works on MariaDB.
- `'kodekloud_pop'@'%'` allows that user to connect from **any host** (`%` is a wildcard) — fine for a lab/challenge environment, but in production this should be scoped to specific hosts or `localhost` wherever possible to reduce attack surface.
- After changing Apache's port, remember firewall rules (see Day 13) also need to allow the new port — a service listening correctly can still be unreachable if the firewall wasn't updated to match.
- `php-fpm` and `httpd`/`mysqld`/`mariadb` are separate services with separate `systemctl status` checks — a broken page can stem from any one of the three being down, so check all of them individually rather than assuming which layer failed.

---

**Stack:** `Linux` `Apache` `PHP` `MariaDB` `LAMP`
