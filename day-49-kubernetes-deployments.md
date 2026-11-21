# Day 49: Deploy Applications with Kubernetes Deployments

**Category:** Kubernetes / Deployments

## Task

The Nautilus DevOps team is using Kubernetes for application management. Create a deployment named `nginx` that runs the `nginx` application from the image `nginx:latest`, with the tag stated explicitly.

`kubectl` on the `jump_host` is already configured to talk to the cluster.

---

## Solution

### Step 1: Create the deployment

```bash
kubectl create deployment nginx --image=nginx:latest
```

Expected output:

```text
deployment.apps/nginx created
```

### Step 2: Verify the deployment

```bash
kubectl get deployment
```

Expected: a row for `nginx` with `READY 1/1` and `AVAILABLE 1` once the image has been pulled and the pod has started.

Extra checks:

```bash
kubectl get pods -l app=nginx
kubectl describe deployment nginx
```

The pod's name looks like `nginx-<replicaset-hash>-<random>`, because the Deployment creates a ReplicaSet and the ReplicaSet creates the pod.

### Equivalent YAML manifest

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      app: nginx
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
        - name: nginx
          image: nginx:latest
```

```bash
kubectl apply -f nginx-deployment.yaml
```

The imperative `kubectl create deployment` command builds the same object, with the label `app=nginx` and the container named `nginx`.

---

## Key Takeaways

- **A Deployment manages pods for you.** It creates a ReplicaSet, which keeps the desired number of pod replicas running. If a pod is deleted or its node fails, the ReplicaSet creates a replacement. A bare pod (Day 48) has no such protection.
- **The ownership chain is Deployment > ReplicaSet > Pod.** You normally only edit the Deployment, and Kubernetes manages the layers below it.
- **Deployments give you rolling updates and rollbacks.** Changing the image (`kubectl set image deployment/nginx nginx=nginx:1.27`) replaces pods gradually, and `kubectl rollout undo deployment/nginx` returns to the previous revision. `kubectl rollout status deployment/nginx` follows progress.
- **Scaling is one command.** `kubectl scale deployment nginx --replicas=3` changes the number of pods without touching a manifest.
- **The selector must match the pod template's labels.** `spec.selector.matchLabels` is how the Deployment finds its pods, and a mismatch makes the API reject the manifest.
- **Imperative vs declarative.** `kubectl create deployment` is quick for a lab task, but a YAML file kept in Git is reproducible and reviewable. `kubectl create deployment ... --dry-run=client -o yaml` generates a manifest to start from.
- **Pin a version tag in real deployments.** `nginx:latest` was required here, but `latest` can change between pulls, which makes rollouts and rollbacks unpredictable.

---

**Stack:** `Kubernetes` `kubectl` `Deployments` `Nginx`
