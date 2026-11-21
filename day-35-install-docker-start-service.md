# Day 35: Install Docker Packages and Start Docker Service

**Category:** Docker / Containers

## Task

The Nautilus DevOps team plans to containerize various applications after a meeting with the application development team. As a first step for testing:

1. Install the `docker-ce` and `docker compose` packages on App Server 1.
2. Start the `docker` service.

---

## Solution

### Step 1: Connect to App Server 1

```bash
ssh tony@stapp01
```

### Step 2: Add the official Docker repository

```bash
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

`docker-ce` isn't in the default CentOS/RHEL repositories, so the Docker repo has to be added first. If `config-manager` isn't found, install the plugin package with `sudo dnf install -y dnf-plugins-core` and retry.

### Step 3: Install Docker Engine and the Compose plugin

```bash
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

- `docker-ce`: the Docker Engine (daemon).
- `docker-ce-cli`: the `docker` command-line client.
- `containerd.io`: the container runtime Docker builds on.
- `docker-buildx-plugin`: extended image-building features.
- `docker-compose-plugin`: Docker Compose v2, used as `docker compose`.

### Step 4: Start and enable the service

```bash
sudo systemctl start docker
sudo systemctl enable docker
```

### Step 5: Verify

```bash
sudo systemctl status docker
docker --version
docker compose version
```

The service should show `active (running)`, and both version commands should print a version number.

---

## Key Takeaways

- **Compose is now a plugin.** The current way to get Compose is the `docker-compose-plugin` package, used as `docker compose` (with a space). The older standalone `docker-compose` binary (with a hyphen) is the legacy v1 approach. The task wording "docker compose" matches the plugin.
- **`start` and `enable` do different things.** `systemctl start docker` runs the service now. `systemctl enable docker` makes it start automatically at boot. Doing both means Docker survives a reboot of the app server.
- **Adding a repo before installing is the standard pattern** for software that isn't in the distro's own repositories. The `.repo` file tells `dnf` where to find and verify the Docker packages.
- **`-y` skips the confirmation prompt.** Without it, `dnf install` stops and waits for you to type `y`, which is fine interactively but will hang in a script or automation.
- **Running `docker` as a normal user needs the `docker` group.** By default the socket is root-only, so non-root users get "permission denied" until they're added with `sudo usermod -aG docker <user>` (and log back in). The task didn't require this, so it's only a heads-up for later days.
- Always confirm with `systemctl status docker` rather than assuming `start` succeeded. A failed start (for example, a conflicting runtime or a bad config) shows up there.

---

**Stack:** `Docker` `Docker Compose` `Linux` `systemd` `dnf`
