# Day 50: Set Resource Limits in Kubernetes Pods

**Category:** Kubernetes / Resource Management

## Task

The Nautilus DevOps team has seen performance problems in some Kubernetes-hosted applications caused by resource constraints, and plans to set limits on resource use. Create a pod with these details:

- Pod name: `httpd-pod`
- Container name: `httpd-container`
- Image: `httpd:latest` (tag specified explicitly)
- Requests: memory `15Mi`, CPU `100m`
- Limits: memory `20Mi`, CPU `100m`

`kubectl` on the `jump_host` is already configured to talk to the cluster.

---

## Solution

### Step 1: Write the pod manifest

```bash
vi pod-resource-limits.yaml
```

Contents:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: httpd-pod
spec:
  containers:
    - name: httpd-container
      image: httpd:latest
      resources:
        requests:
          memory: "15Mi"
          cpu: "100m"
        limits:
          memory: "20Mi"
          cpu: "100m"
```

### Step 2: Create the pod

```bash
kubectl apply -f pod-resource-limits.yaml
```

Expected output:

```text
pod/httpd-pod created
```

### Step 3: Verify

```bash
kubectl get pod httpd-pod
kubectl describe pod httpd-pod
```

In the `describe` output, find the container section and check that it lists:

```text
Limits:
  cpu:     100m
  memory:  20Mi
Requests:
  cpu:        100m
  memory:     15Mi
```

Note that the status isn't guaranteed to be `Running` with these values (see the takeaways). If the pod is stuck or restarting, `kubectl describe pod httpd-pod` and `kubectl get pod httpd-pod -o jsonpath='{.status.containerStatuses[0].lastState}'` show the reason.

---

## Key Takeaways

- **Requests and limits do different jobs.** A **request** is what the scheduler reserves: a pod is placed only on a node with that much unreserved capacity. A **limit** is the ceiling the container may not exceed while running.
- **CPU and memory are enforced differently.** CPU is *compressible*: a container over its CPU limit is throttled and slows down. Memory is *not*: a container that goes over its memory limit is killed by the kernel's OOM killer and shows `OOMKilled`, and Kubernetes restarts it.
- **Units matter.** `100m` means 100 millicores, i.e. 0.1 of a CPU core. `15Mi` and `20Mi` are mebibytes (binary, 1 Mi = 1,048,576 bytes), whereas `M` means megabytes (decimal). Mixing the two up changes the numbers slightly.
- **`20Mi` is a very tight memory limit for `httpd`.** The Apache image can need more than that under load, or even at startup in some configurations, so the container may get `OOMKilled` and go into `CrashLoopBackOff`. The task fixes these values, so apply them as given, but in real use you'd measure actual usage (`kubectl top pod`, needs metrics-server) before choosing limits.
- **QoS class follows from requests and limits.** Here requests don't equal limits for memory (15Mi vs 20Mi), so the pod is `Burstable`. If every request equalled its limit, it would be `Guaranteed`, and with no requests or limits at all it would be `BestEffort`, the first to be evicted under node pressure.
- **Limits can't be edited on a running pod.** A pod's resource fields are immutable, so changing them means deleting and recreating the pod (or changing the pod template of a Deployment, which rolls out new pods).
- **Namespaces can enforce defaults.** `LimitRange` sets default and maximum values per namespace and `ResourceQuota` caps the total, which is how teams stop a single workload from starving others.

---

**Stack:** `Kubernetes` `kubectl` `Resource Limits` `Pods` `YAML`
