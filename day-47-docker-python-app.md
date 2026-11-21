# Day 47: Docker Python App

**Category:** Docker / Containers

## Task

A Python app has to be Dockerized and deployed on App Server 3. The `requirements.txt` file with the app's dependencies is already at `/python_app/src/` on that server.

1. Create a `Dockerfile` in `/python_app` that:
   - uses any `python` image as the base,
   - installs the dependencies from `requirements.txt`,
   - exposes port `5002`,
   - runs the `server.py` script with `CMD`.
2. Build an image named `nautilus/python-app` from it.
3. Create a container named `pythonapp_nautilus` that maps container port `5002` to host port `8098`.
4. Test the app with `curl` on App Server 3.

---

## Solution

### Step 1: Connect and look at the layout

```bash
ssh banner@stapp03
cd /python_app/
ls -R
```

`ls -R` confirms where `requirements.txt` and `server.py` live. Here both are under `src/`, which matters for the `COPY` paths below.

### Step 2: Create the Dockerfile

```bash
sudo vi Dockerfile
```

Contents:

```dockerfile
FROM python:3.11.14-alpine

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 5002

CMD ["python", "server.py"]
```

How it maps to the requirements:

- `FROM python:3.11.14-alpine`: a `python` base image (Alpine variant, small).
- `WORKDIR /app`: sets the working directory inside the image, and creates it.
- `COPY src/requirements.txt .` followed by `RUN pip install ...`: installs the dependencies.
- `COPY src/ .`: copies the app code (including `server.py`) after the install step.
- `EXPOSE 5002`: documents the port the app listens on.
- `CMD ["python", "server.py"]`: starts the app when the container runs.

### Step 3: Build the image

```bash
docker build -t nautilus/python-app .
```

Run it from `/python_app`, so that `src/` is inside the build context.

### Step 4: Run the container

```bash
docker run -d --name pythonapp_nautilus -p 8098:5002 nautilus/python-app
```

### Step 5: Test

```bash
docker ps
curl http://localhost:8098/
```

`docker ps` should show `pythonapp_nautilus` as `Up` with `0.0.0.0:8098->5002/tcp`, and `curl` should return the app's response.

---

## Key Takeaways

- **Copy `requirements.txt` first, install, then copy the rest of the code.** Docker caches each layer. When only the app code changes, the slow `pip install` layer is reused from cache, so rebuilds are much faster. Copying everything first would reinstall dependencies on every code change.
- **`--no-cache-dir` keeps the image smaller.** It stops pip from storing downloaded packages in the image layer.
- **`COPY` paths are relative to the build context.** The context is the directory passed to `docker build` (`.` = `/python_app`), so the files are referenced as `src/...`, not `/python_app/src/...`.
- **`EXPOSE` only documents the port.** The mapping that makes the app reachable is `-p 8098:5002` (host:container) in `docker run`.
- **The app must listen on `0.0.0.0` inside the container.** If `server.py` binds only to `127.0.0.1`, the port mapping works but connections from outside the container are refused. For Flask this means `app.run(host="0.0.0.0", port=5002)`.
- **The exec form of `CMD` (`["python", "server.py"]`) is preferred.** It runs Python directly as the main process, so signals such as `docker stop` reach it, instead of going through a shell.
- **Alpine images are small but can complicate some packages.** Libraries that need compiling or that ship glibc-only wheels may fail on Alpine (musl). If `pip install` fails, switching to a `-slim` tag usually fixes it.
- **Image names with a slash are `namespace/repository`.** `nautilus/python-app` has no registry prefix, so it stays local unless it's re-tagged for a registry (see Day 38).

---

**Stack:** `Docker` `Dockerfile` `Python` `Containers`
