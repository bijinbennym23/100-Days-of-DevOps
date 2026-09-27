# Day 17: Install and Configure PostgreSQL

**Category:** Databases / PostgreSQL

## Task

Install PostgreSQL, create a new database user, create a new database, and grant that user full privileges on it.

---

## Solution

### Step 1: Install PostgreSQL

```bash
sudo yum install postgresql-server postgresql-contrib -y
sudo postgresql-setup initdb
sudo systemctl enable --now postgresql
```

### Step 2: Switch to the postgres system user

```bash
sudo su - postgres
```

PostgreSQL creates a `postgres` OS user during install, which owns the database cluster and has full admin rights inside PostgreSQL by default — day-to-day admin tasks are typically run as this user rather than as root.

### Step 3: Open the PostgreSQL interactive shell

```bash
psql
```

### Step 4: Create a new database user

```sql
CREATE USER kodekloud_joy WITH PASSWORD 'ksH85UJjhb';
```

### Step 5: Create a new database

```sql
CREATE DATABASE kodekloud_db10;
```

### Step 6: Grant the user full privileges on the database

```sql
GRANT ALL PRIVILEGES ON DATABASE kodekloud_db10 TO kodekloud_joy;
```

### Step 7: Verify

```sql
\du
\l
```

`\du` lists roles/users, `\l` lists databases along with their owners and access privileges.

---

## Key Takeaways

- `CREATE USER ... WITH PASSWORD` creates a login-capable role — in PostgreSQL, "users" and "roles" are the same underlying object; `CREATE USER` is shorthand for a role with `LOGIN` enabled.
- `GRANT ALL PRIVILEGES ON DATABASE` grants database-level privileges (connect, create schemas, etc.) — it does **not** automatically grant privileges on tables *within* that database. Table-level access still needs its own `GRANT` statements once tables exist, or the user will connect successfully but be unable to touch the data.
- Running admin commands as the `postgres` OS user relies on PostgreSQL's default `peer` authentication for local connections — the OS username has to match the PostgreSQL role name for passwordless local login to work, which is why `sudo su - postgres` is the standard path in, not any arbitrary user.
- SQL statements in `psql` must end with a semicolon — a command that appears to "hang" after Enter is almost always just waiting for the terminating `;`.

---

**Stack:** `PostgreSQL` `Databases` `Linux`
