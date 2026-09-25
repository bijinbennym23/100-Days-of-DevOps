# Day 11: Install and Configure Tomcat Server

**Category:** Linux / Application Servers

## Task

Install Tomcat, configure it, deploy a `ROOT.war` application copied over from the jump host, and verify the app is reachable.

---

## Solution

### Step 1: Install Tomcat

```bash
yum info tomcat
sudo yum install tomcat -y
```

### Step 2: Review/edit Tomcat's startup and server config

```bash
sudo vi /etc/tomcat/conf.d/java-9-start-up-parameters.conf
sudo vi /usr/share/tomcat/conf/server.xml
```

### Step 3: Restart Tomcat to pick up config changes

```bash
sudo systemctl restart tomcat
```

### Step 4: Copy the WAR file from the jump host

From the jump host:

```bash
sudo scp /tmp/ROOT.war steve@stapp02:/tmp
```

`scp` prompted for `steve`'s password here — key-based auth (see Day 7) wasn't set up for this hop, so it fell back to password authentication.

### Step 5: Deploy the WAR file into Tomcat's webapps directory

On the target server:

```bash
cd /usr/share/tomcat/webapps/
ls -la
sudo mv /tmp/ROOT.war /usr/share/tomcat/webapps/
sudo chown steve:steve /usr/share/tomcat/webapps/ROOT.war
```

### Step 6: Restart Tomcat to deploy the app

```bash
sudo systemctl restart tomcat
```

### Step 7: Verify the app is reachable

```bash
curl http://stapp02:3000
```

---

## Key Takeaways

- Dropping a `.war` file into Tomcat's `webapps/` directory is enough to trigger auto-deployment — Tomcat explodes and deploys it on the next start/restart without needing a separate deploy command.
- `ROOT.war` specifically deploys to the server's root context (`/`) rather than a sub-path — this is why the app was reachable directly at `http://stapp02:3000` instead of `http://stapp02:3000/ROOT`.
- File ownership matters after a `sudo mv`: the moved file inherits root ownership by default, so `chown steve:steve` was needed to match the user Tomcat runs as — a mismatch here can cause Tomcat to fail loading the app silently or throw permission errors in its logs.
- The password prompt during `scp` is a signal, not just friction — it's worth setting up SSH keys (Day 7) between the jump host and app servers if this transfer is going to happen repeatedly, rather than typing a password each time.
- Always restart the service *after* the file is in place with correct ownership — restarting too early (before the `chown`) can leave Tomcat holding a lock on a file it can't properly read.

---

**Stack:** `Linux` `Tomcat` `Java` `Application Servers`
