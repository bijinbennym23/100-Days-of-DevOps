# Day 42: Create a Docker Network

**Category:** Docker / Networking

## Task

The Nautilus DevOps team is setting up several Docker environments for different applications. A ticket asks for some Docker networks to be created for later use. On App Server 3 in the Stratos DC:

1. Create a Docker network named `ecommerce`.
2. Configure it to use the `bridge` driver.
3. Set the subnet to `10.10.1.0/24` and the IP range to `10.10.1.0/24`.

---

## Solution

### Step 1: Connect to App Server 3

```bash
ssh banner@stapp03
```

### Step 2: Create the network

```bash
docker network create -d bridge --subnet=10.10.1.0/24 --ip-range=10.10.1.0/24 ecommerce
```

- `-d bridge` selects the bridge driver (the default, but stated explicitly because the task asks for it).
- `--subnet=10.10.1.0/24` sets the network's address range.
- `--ip-range=10.10.1.0/24` limits which addresses Docker hands out to containers. Here it covers the whole subnet.
- `ecommerce` is the network name.

### Step 3: Confirm the network exists

```bash
docker network ls
```

Expected: a row for `ecommerce` with driver `bridge` and scope `local`.

### Step 4: Check the subnet and IP range

```bash
docker network inspect ecommerce
```

In the output, look under `IPAM` > `Config` for:

```json
"Subnet": "10.10.1.0/24",
"IPRange": "10.10.1.0/24"
```

---

## Key Takeaways

- **A bridge network is a private virtual switch on a single host.** Containers attached to it can reach each other and the outside world (through NAT), but aren't reachable from outside unless a port is published with `-p`.
- **User-defined bridges beat the default `bridge` network.** On a custom network, containers can reach each other **by name** through Docker's built-in DNS. The default `bridge` network only supports IP addresses (or the legacy `--link`).
- **`--subnet` and `--ip-range` are different things.** The subnet is the whole address block for the network. The IP range is the slice Docker may assign automatically. Setting the range to a smaller block, such as `10.10.1.128/25`, leaves the rest of the subnet free for containers you give a fixed address with `--ip`.
- **The range must sit inside the subnet.** An `--ip-range` outside the subnet makes `docker network create` fail.
- **Avoid overlapping with existing networks.** Docker rejects a subnet that overlaps another Docker network, and a range that overlaps your host's real network can cause routing problems. `docker network inspect` on the existing networks shows what's already in use.
- **The gateway takes the first address.** Docker assigns `10.10.1.1` to the bridge itself, so containers start from `10.10.1.2`.
- **Attach containers at run time.** Use `docker run --network ecommerce ...`, or connect a running container with `docker network connect ecommerce <container>`.
- **Networks are local to the host.** A bridge network on App Server 3 doesn't exist on the other servers. Spanning hosts needs an overlay network (Swarm) or another networking layer.

---

**Stack:** `Docker` `Networking` `Bridge Network` `Containers`
