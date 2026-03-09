# Recommended `database/` Directory Structure

```
database/
│
├── schema/
│   ├── users.sql
│   ├── plants.sql
│   ├── gardens.sql
│   ├── marketplace.sql
│   └── notifications.sql
│
├── migrations/
│   ├── 001_create_users_table.sql
│   ├── 002_create_plants_table.sql
│   ├── 003_create_gardens_table.sql
│   ├── 004_create_orders_table.sql
│
├── seeds/
│   ├── plants_seed.sql
│   ├── products_seed.sql
│   └── sample_users.sql
│
├── views/
│   └── plant_health_view.sql
│
├── procedures/
│   └── calculate_health_score.sql
│
├── diagrams/
│   └── er-diagram.png
│
├── docker/
│   └── init.sql
│
└── README.md
```

---

# What Each Folder Does

## `schema/`

Contains **table definitions**.

Example:

```
users.sql
plants.sql
garden_plants.sql
orders.sql
```

Example file:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    password_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

# `migrations/`

Tracks **database version changes**.

Example:

```
001_create_users_table.sql
002_create_plants_table.sql
003_add_health_score.sql
```

This is useful when your database evolves.

---

# `seeds/`

Sample data for development.

Example:

```
plants_seed.sql
products_seed.sql
```

Example:

```sql
INSERT INTO plants (plant_name, soil_type)
VALUES ('Tomato', 'Loamy');
```

This helps the **Android app and API test immediately**.

---

# `views/`

Database **views for analytics or AI data**.

Example:

```
plant_health_view.sql
```

Example:

```sql
CREATE VIEW plant_health_view AS
SELECT
gp.id,
phd.soil_moisture,
phd.temperature,
phd.health_score
FROM garden_plants gp
JOIN plant_health_data phd
ON gp.id = phd.garden_plant_id;
```

---

# `procedures/`

Stored procedures for calculations.

Example:

```
calculate_health_score.sql
```

Example:

```sql
CREATE FUNCTION calculate_health_score(...)
RETURNS INTEGER
```

---

# `diagrams/`

System diagrams.

```
er-diagram.png
database-architecture.png
```

Teachers love seeing this.

---

# `docker/`

Used when running database via **Docker**.

Example:

```
init.sql
```

This automatically creates tables when the container starts.

---

# `database/README.md`

Explain how to set up the database.

Example:

```
# Database Setup

1. Install PostgreSQL
2. Create database plantive_db
3. Run schema files
4. Run seed files
```

---

# Final Example in Your Repo

```
plantive-ecosystem
│
├── mobile/
│
├── backend/
│
├── ai/
│
├── web/
│
├── database/
│   ├── schema/
│   ├── migrations/
│   ├── seeds/
│   ├── views/
│   ├── procedures/
│   ├── diagrams/
│   └── README.md
│
├── docs/
│
└── README.md
```

---

# Pro Tip (Important)

Keep **database logic separate from backend code**.
Backend should only call queries, not define schema.

Your backend folder will look like:

```
backend/api-server
│
├── controllers
├── routes
├── models
├── services
└── config
```

---