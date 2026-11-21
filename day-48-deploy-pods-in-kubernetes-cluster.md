# Day 48: Deploy Pods in Kubernetes Cluster

**Category:** Kubernetes / Pods

## Task

The Nautilus DevOps team is starting with Kubernetes for application management. Create a pod as follows:

1. Name it `pod-nginx`, using the `nginx` image with the `latest` tag, written explicitly as `nginx:latest`.
2. Set the label `app` to `nginx_app`, and name the container `nginx-container`.

`kubectl` on the `jump_host` is already configured to talk to the cluster.

---

## Solution

### Step 1: Write the pod manifest

On the jump host:

```bash
vi nginx.yaml
```

Contents:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-nginx
  labels:
    app: nginx_app
spec:
  containers:
    - name: nginx-container
      image: nginx:latest
```

What each part does:

- `apiVersion: v1` and `kind: Pod` declare the object type (Pods belong to the core `v1` API group).
- `metadata.name` is the pod's name, `pod-nginx`.
- `metadata.labels` attaches the key/value label `app: nginx_app`.
- `spec.containers` lists the containers in the pod. Here there is one, named `nginx-container`, running `nginx:latest`.

### Step 2: Create the pod

```bash
kubectl apply -f nginx.yaml
```

Expected output:

```text
pod/pod-nginx created
```

### Step 3: Verify

```bash
kubectl get pod
```

Wait for the `STATUS` column to read `Running` (it may show `ContainerCreating` for a few seconds while the image is pulled).

Extra checks:

```bash
kubectl get pod pod-nginx --show-labels
kubectl describe pod pod-nginx
```

`--show-labels` confirms `app=nginx_app`, and `describe` shows the container name, image and recent events.

### Quick alternative without a file

```bash
kubectl run pod-nginx --image=nginx:latest --labels=app=nginx_app
```

This creates the pod directly, but the container takes the pod's name (`pod-nginx`) rather than `nginx-container`. Since the task requires that container name, the YAML manifest is the right route here. To generate a starting manifest without writing it by hand:

```bash
kubectl run pod-nginx --image=nginx:latest --labels=app=nginx_app --dry-run=client -o yaml > nginx.yaml
```

Then edit the container name in the file before applying.

---

## Key Takeaways

- **A Pod is the smallest deployable unit in Kubernetes.** It wraps one or more containers that share a network namespace and storage. Most pods hold a single container.
- **YAML indentation is syntax.** Use spaces, never tabs, and keep list items (`- name: ...`) and their keys aligned. A mismatched indent is the most common reason `kubectl apply` fails with a parse error.
- **Pod name, container name and labels are separate things.** The pod name identifies the object in the cluster, the container name identifies the container inside it, and labels are free-form key/value tags used for selection (by Services, Deployments and `kubectl get -l`).
- **Always set an explicit image tag.** `nginx:latest` is what the task asks for. Leaving the tag off also resolves to `latest`, but explicit tags make the manifest self-documenting. In production, pinning a specific version is safer because `latest` can change.
- **`kubectl apply` is declarative; `kubectl create` is imperative.** `apply` creates the object if it's missing and updates it if it exists. Re-running it with a changed manifest works, while `create` fails when the object already exists.
- **A bare pod isn't self-healing.** If the node dies or the pod is deleted, nothing recreates it. Deployments and ReplicaSets manage that, which is the next step up from this task.
- **Use `kubectl describe` and `kubectl logs` to debug.** `ErrImagePull` or `ImagePullBackOff` in the status points to a wrong image name or tag, and the Events section at the bottom of `describe` says why.

---

**Stack:** `Kubernetes` `kubectl` `Pods` `YAML` `Nginx`
