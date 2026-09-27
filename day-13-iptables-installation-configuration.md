# Day 13: IPtables Installation And Configuration

**Category:** Linux / Security / Networking

## Task

Apache is running on port `6400` on the app hosts, currently open to everyone with no firewall in place. Lock it down:

1. Install `iptables` and its dependencies on each app host.
2. Block incoming port `6400` for everyone **except** the load balancer (LBR) host.
3. Make sure the rules survive a reboot.

---

## Solution

*(Repeat on each app host — example uses `stapp01`.)*

### Step 1: Connect to the app host

```bash
ssh tony@stapp01
```

### Step 2: Install iptables and the persistence service

```bash
sudo yum install iptables iptables-services -y
```

`iptables-services` provides the systemd unit and the `service iptables save` command needed for persistence — plain `iptables` alone only manages the in-memory ruleset.

### Step 3: Enable and start the service

```bash
sudo systemctl enable --now iptables
sudo systemctl status iptables
```

### Step 4: Check for a pre-existing blanket REJECT/DROP rule

```bash
sudo iptables -L -n --line-numbers
```

Many CentOS/RHEL images ship with a catch-all `REJECT` rule already in place. Any rule you add for port `6400` must sit **above** this rule in the chain — `iptables` evaluates rules top-to-bottom and stops at the first match, so a rule placed below a blanket REJECT never gets a chance to apply.

### Step 5: Insert the allow rule for the LBR host

```bash
sudo iptables -I INPUT <position> -p tcp -s 172.16.238.14 --dport 6400 -j ACCEPT
```

`-I INPUT <position>` **inserts** at a specific line number (rather than `-A`, which appends to the end) — this is what lets you place the rule above the existing blanket REJECT. Use the line numbers from Step 4 to pick the right position.

### Step 6: Insert the drop rule for everyone else, immediately after

```bash
sudo iptables -I INPUT <position+1> -p tcp --dport 6400 -j DROP
```

Scoped specifically to `--dport 6400` — not a blanket drop-all. A bare `-j DROP` with no port filter risks blocking SSH and other legitimate traffic if it lands above the rules that allow them.

### Step 7: Verify the final rule order

```bash
sudo iptables -L -n
```

Confirm the order is: **LBR allow** → **port 6400 drop (everyone else)** → **existing blanket REJECT** (which now only applies to traffic that isn't `6400`).

### Step 8: Persist the rules

```bash
sudo service iptables save
```

This writes the current in-memory ruleset to `/etc/sysconfig/iptables`, which `iptables-services` reloads automatically on boot.

### Step 9: Test from both sides

```bash
curl http://stapp01:6400
```

- From the **jump host** (not the LBR) → should **fail** (blocked by the `DROP` rule).
- From the **LBR** (`172.16.238.14`) → should **succeed** (allowed by the explicit `ACCEPT` rule).

### Step 10: Repeat on the remaining app hosts

Same steps, same rule order, on every app server that needs the port locked down.

---

## Key Takeaways

- **Rule order is everything** in `iptables` — the first matching rule wins, so an otherwise-correct rule placed below a blanket REJECT/DROP will never fire.
- Use `-I INPUT <N>` (insert at position) rather than `-A INPUT` (append to end) when a rule needs to land above existing rules like a default REJECT.
- Scope the deny as narrowly as possible (`--dport 6400`, not a bare `-j DROP`) — a blanket drop is one misplaced rule away from locking out SSH or other essential traffic.
- `iptables -L -n --line-numbers` is essential before *and* after any insert/delete — line numbers shift every time a rule is added or removed, so re-check before making the next change.
- `iptables-services` + `service iptables save` is the standard persistence combo on CentOS/RHEL; without saving, rules only live in memory and are lost on reboot.
- `firewalld` and `iptables-services` shouldn't run at the same time — on CentOS/RHEL 7+, `firewalld` is the default and can conflict with manually managed `iptables` rules if both are active. Confirm only one is managing the host's firewall.
- Test from **both** an allowed source and a denied source — confirming the block alone isn't enough; confirming the exception still works is just as important.

---

**Stack:** `Linux` `iptables` `Security` `Networking` `Firewall`
