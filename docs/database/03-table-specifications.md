# Plantive Database Table Specifications

**Document:** `03-table-specifications.md`
**Project:** Plantive — Your Smart Gardening Tool
**Database:** PostgreSQL
**ORM:** SQLModel
**Migration Tool:** Alembic
**Driver:** asyncpg
**Status:** Design Specification
**Version:** 1.0

---

# 1. Purpose

This document defines the detailed database specifications for the Plantive application.

It describes the structure and behavior of each database table, including:

* Table purpose
* Columns
* PostgreSQL data types
* SQLModel/Python types
* Nullability
* Default values
* Primary keys
* Foreign keys
* Unique constraints
* Check constraints
* Timestamp fields
* Soft-deletion behavior
* Ownership rules
* Important business rules

This document is intended to be used as a reference when implementing:

```text
SQLModel Models
       ↓
Alembic Migrations
       ↓
Repositories
       ↓
Services
       ↓
Tests
```

The database remains the source of truth for structural data integrity.

---

# 2. Database Conventions

## 2.1 Primary Keys

Plantive uses UUIDs for primary keys on major entities.

Example:

```text
123e4567-e89b-12d3-a456-426614174000
```

Recommended PostgreSQL type:

```text
UUID
```

Recommended SQLModel/Python type:

```python
UUID
```

---

## 2.2 Foreign Keys

Foreign keys follow the naming convention:

```text
<entity>_id
```

Examples:

```text
user_id
garden_id
plant_id
order_id
product_id
post_id
```

---

## 2.3 Timestamps

Persistent entities should use timezone-aware timestamps.

PostgreSQL:

```text
TIMESTAMPTZ
```

Python:

```python
datetime
```

All application timestamps should be stored and processed in UTC.

---

## 2.4 Boolean Naming

Boolean columns should use descriptive `is_` or `has_` prefixes where appropriate.

Examples:

```text
is_active
is_verified
```

---

## 2.5 Table Naming

Tables use plural `snake_case` names.

Examples:

```text
users
gardens
plants
orders
order_items
plant_health_records
```

---

# 3. Table Inventory

|  # | Table                        | Domain         | Status  |
| -: | ---------------------------- | -------------- | ------- |
|  1 | `users`                      | Identity       | Core    |
|  2 | `gardens`                    | Gardening      | Planned |
|  3 | `plants`                     | Gardening      | Planned |
|  4 | `plant_health_records`       | Gardening      | Planned |
|  5 | `plant_environment_records`  | Gardening      | Planned |
|  6 | `care_reminders`             | Gardening      | Planned |
|  7 | `fertilizer_recommendations` | Gardening      | Planned |
|  8 | `categories`                 | Marketplace    | Planned |
|  9 | `products`                   | Marketplace    | Planned |
| 10 | `services`                   | Marketplace    | Planned |
| 11 | `orders`                     | Marketplace    | Planned |
| 12 | `order_items`                | Marketplace    | Planned |
| 13 | `posts`                      | Community      | Planned |
| 14 | `comments`                   | Community      | Planned |
| 15 | `admin_audit_logs`           | Administration | Future  |

---

# 4. `users`

## 4.1 Purpose

The `users` table stores registered Plantive user accounts.

It is the central identity entity in the application.

Users may own or create resources across the platform, including:

```text
Users
├── Gardens
├── Orders
├── Posts
└── Comments
```

---

## 4.2 Columns

| Column            | PostgreSQL Type | Python / SQLModel Type | Nullable | Default    | Constraints |
| ----------------- | --------------- | ---------------------- | -------- | ---------- | ----------- |
| `id`              | `UUID`          | `UUID`                 | No       | generated  | PK          |
| `email`           | `VARCHAR(320)`  | `str`                  | No       | —          | UNIQUE      |
| `hashed_password` | `VARCHAR`       | `str`                  | No       | —          | —           |
| `full_name`       | `VARCHAR(100)`  | `str`                  | No       | —          | —           |
| `avatar_url`      | `TEXT`          | `str \| None`          | Yes      | `NULL`     | —           |
| `role`            | `VARCHAR(20)`   | Enum / `str`           | No       | `gardener` | CHECK       |
| `is_active`       | `BOOLEAN`       | `bool`                 | No       | `true`     | —           |
| `is_verified`     | `BOOLEAN`       | `bool`                 | No       | `false`    | —           |
| `created_at`      | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now    | —           |
| `updated_at`      | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now    | —           |

---

## 4.3 `id`

The primary identifier of the user.

```text
Type: UUID
Primary Key: Yes
Nullable: No
```

The UUID is exposed through the API as the user's public identifier.

---

## 4.4 `email`

The user's login and communication email address.

Requirements:

* Required
* Unique
* Normalized before persistence
* Must not contain leading/trailing whitespace
* Maximum length should follow the selected email validation policy

Database constraint:

```text
UNIQUE(email)
```

The application should normalize email addresses consistently before lookup and storage.

---

## 4.5 `hashed_password`

Stores the password hash.

The application must **never store plaintext passwords**.

The current project uses:

```text
pwdlib[argon2]
```

Therefore, password hashing should occur in the service/security layer before the value reaches the repository.

Database:

```text
hashed_password
```

not:

```text
password
```

---

## 4.6 `full_name`

Stores the user's display name.

Current API rule:

```text
Minimum: 2 characters
Maximum: 100 characters
```

Leading/trailing whitespace should be removed before persistence.

---

## 4.7 `avatar_url`

Stores the URL/reference to the user's avatar.

Example:

```text
https://cdn.plantive.com/avatars/{user_id}.webp
```

This column stores the **reference**, not the binary image.

The actual file should be stored in:

```text
Object Storage / File Storage
```

rather than PostgreSQL.

---

## 4.8 `role`

Defines the user's authorization role.

Current roles:

```text
gardener
admin
```

Recommended application representation:

```python
class UserRole(str, Enum):
    GARDENER = "gardener"
    ADMIN = "admin"
```

The database should prevent unsupported role values.

Conceptual constraint:

```sql
CHECK (role IN ('gardener', 'admin'))
```

---

## 4.9 `is_active`

Determines whether the account is active.

```text
true  → active
false → deactivated
```

Normal account deletion is implemented as:

```text
is_active = false
```

The row is retained.

---

## 4.10 `is_verified`

Indicates whether the user's email/account verification requirement has been satisfied.

```text
true  → verified
false → not verified
```

Normal users must not be allowed to modify this field through their self-profile API.

---

## 4.11 `created_at`

Timestamp when the account was created.

Immutable after creation.

---

## 4.12 `updated_at`

Timestamp of the latest relevant user record modification.

Updated whenever mutable user information changes.

---

## 4.13 User Constraints

### Primary Key

```text
users.id
```

### Unique

```text
users.email
```

### Check

```text
role IN ('gardener', 'admin')
```

---

## 4.14 User Business Rules

1. Email must be unique.
2. Passwords must never be stored in plaintext.
3. Users cannot modify their own `role`.
4. Users cannot modify their own `is_active`.
5. Users cannot modify their own `is_verified`.
6. Deactivation normally uses soft deletion.
7. Deactivated users must not authenticate successfully.
8. Deactivating a user must revoke their active refresh-token state.
9. Admin self-demotion is prohibited.
10. Hard deletion is exceptional.

---

# 5. `gardens`

## 5.1 Purpose

Stores gardens created and owned by users.

Relationship:

```text
User
 │
 └──< Garden
```

---

## 5.2 Columns

| Column        | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints     |
| ------------- | --------------- | ---------------------- | -------- | --------- | --------------- |
| `id`          | `UUID`          | `UUID`                 | No       | generated | PK              |
| `user_id`     | `UUID`          | `UUID`                 | No       | —         | FK → `users.id` |
| `name`        | `VARCHAR(100)`  | `str`                  | No       | —         | —               |
| `description` | `TEXT`          | `str \| None`          | Yes      | `NULL`    | —               |
| `created_at`  | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —               |
| `updated_at`  | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —               |

---

## 5.3 Ownership

```text
gardens.user_id → users.id
```

A garden belongs to exactly one user.

A user may own multiple gardens.

---

## 5.4 Business Rules

* `user_id` is required.
* Users can access only their own gardens unless an authorized administrator is performing an administrative operation.
* Garden ownership should not silently change during normal updates.
* Soft-deleted users should not automatically cause historical gardens to disappear.

---

# 6. `plants`

## 6.1 Purpose

Represents a plant managed inside a user's garden.

Relationship:

```text
User
 │
 └──< Garden
          │
          └──< Plant
```

---

## 6.2 Columns

| Column          | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints       |
| --------------- | --------------- | ---------------------- | -------- | --------- | ----------------- |
| `id`            | `UUID`          | `UUID`                 | No       | generated | PK                |
| `garden_id`     | `UUID`          | `UUID`                 | No       | —         | FK → `gardens.id` |
| `name`          | `VARCHAR(100)`  | `str`                  | No       | —         | —                 |
| `species`       | `VARCHAR(150)`  | `str \| None`          | Yes      | `NULL`    | —                 |
| `description`   | `TEXT`          | `str \| None`          | Yes      | `NULL`    | —                 |
| `health_status` | `VARCHAR(30)`   | Enum / `str`           | No       | —         | CHECK             |
| `planted_at`    | `TIMESTAMPTZ`   | `datetime \| None`     | Yes      | `NULL`    | —                 |
| `created_at`    | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —                 |
| `updated_at`    | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —                 |

---

## 6.3 Ownership

A plant belongs to a garden.

```text
plants.garden_id → gardens.id
```

The application must determine the owner through:

```text
Plant
  ↓
Garden
  ↓
User
```

---

## 6.4 Business Rules

A user must not be able to access another user's plant simply by knowing the plant UUID.

Authorization must verify the ownership chain.

---

# 7. `plant_health_records`

## 7.1 Purpose

Stores historical health observations for plants.

---

## 7.2 Columns

| Column          | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints      |
| --------------- | --------------- | ---------------------- | -------- | --------- | ---------------- |
| `id`            | `UUID`          | `UUID`                 | No       | generated | PK               |
| `plant_id`      | `UUID`          | `UUID`                 | No       | —         | FK → `plants.id` |
| `health_status` | `VARCHAR(30)`   | Enum / `str`           | No       | —         | —                |
| `health_score`  | `SMALLINT`      | `int`                  | Yes      | `NULL`    | 0–100            |
| `notes`         | `TEXT`          | `str \| None`          | Yes      | `NULL`    | —                |
| `recorded_at`   | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —                |

---

## 7.3 Constraints

If `health_score` is stored:

```text
0 <= health_score <= 100
```

This should be enforced by validation and preferably by a database check constraint.

---

## 7.4 Purpose of Historical Records

Health records should normally be append-oriented.

Instead of continuously overwriting:

```text
plant.health_status
```

the application can maintain historical observations:

```text
Plant
 │
 ├── Health Record
 ├── Health Record
 ├── Health Record
 └── Health Record
```

This supports future analytics and plant-health history.

---

# 8. `plant_environment_records`

## 8.1 Purpose

Stores environmental observations associated with a plant.

The current specification describes simulated environmental monitoring.

---

## 8.2 Proposed Columns

| Column          | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints      |
| --------------- | --------------- | ---------------------- | -------- | --------- | ---------------- |
| `id`            | `UUID`          | `UUID`                 | No       | generated | PK               |
| `plant_id`      | `UUID`          | `UUID`                 | No       | —         | FK → `plants.id` |
| `temperature`   | `NUMERIC(5,2)`  | `Decimal \| None`      | Yes      | `NULL`    | —                |
| `humidity`      | `NUMERIC(5,2)`  | `Decimal \| None`      | Yes      | `NULL`    | —                |
| `soil_moisture` | `NUMERIC(5,2)`  | `Decimal \| None`      | Yes      | `NULL`    | —                |
| `light_level`   | `NUMERIC(8,2)`  | `Decimal \| None`      | Yes      | `NULL`    | —                |
| `recorded_at`   | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —                |

---

## 8.3 Design Note

These columns are **proposed** because the current API specification does not yet define exact environmental measurements or units.

Before implementation, the project should explicitly define:

```text
temperature → Celsius?
humidity → percentage?
soil_moisture → percentage?
light_level → lux?
```

Do not create ambiguous numeric fields without defining their units.

---

# 9. `care_reminders`

## 9.1 Purpose

Stores scheduled plant-care reminders.

Examples:

```text
Water plant
Fertilize plant
Check soil
Move plant
Prune plant
```

---

## 9.2 Proposed Columns

| Column          | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints      |
| --------------- | --------------- | ---------------------- | -------- | --------- | ---------------- |
| `id`            | `UUID`          | `UUID`                 | No       | generated | PK               |
| `plant_id`      | `UUID`          | `UUID`                 | No       | —         | FK → `plants.id` |
| `title`         | `VARCHAR(150)`  | `str`                  | No       | —         | —                |
| `description`   | `TEXT`          | `str \| None`          | Yes      | `NULL`    | —                |
| `reminder_type` | `VARCHAR(30)`   | Enum / `str`           | No       | —         | —                |
| `scheduled_at`  | `TIMESTAMPTZ`   | `datetime`             | No       | —         | —                |
| `is_completed`  | `BOOLEAN`       | `bool`                 | No       | `false`   | —                |
| `created_at`    | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —                |
| `updated_at`    | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —                |

---

## 9.3 Business Rules

A reminder belongs to a plant.

Ownership is therefore resolved through:

```text
Reminder
  ↓
Plant
  ↓
Garden
  ↓
User
```

A user must only be able to manage reminders for plants they own.

---

# 10. `fertilizer_recommendations`

## 10.1 Purpose

Stores fertilizer recommendations associated with plant care.

---

## 10.2 Proposed Columns

| Column           | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints      |
| ---------------- | --------------- | ---------------------- | -------- | --------- | ---------------- |
| `id`             | `UUID`          | `UUID`                 | No       | generated | PK               |
| `plant_id`       | `UUID`          | `UUID`                 | No       | —         | FK → `plants.id` |
| `recommendation` | `TEXT`          | `str`                  | No       | —         | —                |
| `reason`         | `TEXT`          | `str \| None`          | Yes      | `NULL`    | —                |
| `created_at`     | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —                |

---

## 10.3 Design Note

If fertilizer recommendations are generated dynamically and do not need historical storage, this table may not be necessary.

The decision should be based on whether Plantive needs:

```text
Recommendation history
Analytics
Repeated display
Auditing
AI result persistence
```

---

# 11. `categories`

## 11.1 Purpose

Stores marketplace product categories.

Examples:

```text
Plants
Gardening Tools
Fertilizers
Pots
Seeds
```

---

## 11.2 Columns

| Column        | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints |
| ------------- | --------------- | ---------------------- | -------- | --------- | ----------- |
| `id`          | `UUID`          | `UUID`                 | No       | generated | PK          |
| `name`        | `VARCHAR(100)`  | `str`                  | No       | —         | UNIQUE      |
| `description` | `TEXT`          | `str \| None`          | Yes      | `NULL`    | —           |
| `is_active`   | `BOOLEAN`       | `bool`                 | No       | `true`    | —           |
| `created_at`  | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —           |
| `updated_at`  | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —           |

---

# 12. `products`

## 12.1 Purpose

Represents physical products available through the marketplace.

---

## 12.2 Columns

| Column           | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints          |
| ---------------- | --------------- | ---------------------- | -------- | --------- | -------------------- |
| `id`             | `UUID`          | `UUID`                 | No       | generated | PK                   |
| `category_id`    | `UUID`          | `UUID`                 | No       | —         | FK → `categories.id` |
| `name`           | `VARCHAR(200)`  | `str`                  | No       | —         | —                    |
| `description`    | `TEXT`          | `str \| None`          | Yes      | `NULL`    | —                    |
| `price`          | `NUMERIC(12,2)` | `Decimal`              | No       | —         | >= 0                 |
| `stock_quantity` | `INTEGER`       | `int`                  | No       | `0`       | >= 0                 |
| `is_active`      | `BOOLEAN`       | `bool`                 | No       | `true`    | —                    |
| `created_at`     | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —                    |
| `updated_at`     | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —                    |

---

## 12.3 Price

Monetary values should use:

```text
NUMERIC
```

rather than floating-point types.

Do not use:

```text
FLOAT
DOUBLE PRECISION
```

for financial amounts where exact decimal arithmetic is required.

---

## 12.4 Stock

Stock quantity must not be negative.

Database-level rule:

```text
stock_quantity >= 0
```

---

# 13. `services`

## 13.1 Purpose

Represents gardening services available through Plantive.

Examples:

```text
Garden Maintenance
Plant Consultation
Garden Setup
Landscaping
```

---

## 13.2 Columns

| Column        | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints |
| ------------- | --------------- | ---------------------- | -------- | --------- | ----------- |
| `id`          | `UUID`          | `UUID`                 | No       | generated | PK          |
| `name`        | `VARCHAR(200)`  | `str`                  | No       | —         | —           |
| `description` | `TEXT`          | `str \| None`          | Yes      | `NULL`    | —           |
| `price`       | `NUMERIC(12,2)` | `Decimal`              | No       | —         | >= 0        |
| `is_active`   | `BOOLEAN`       | `bool`                 | No       | `true`    | —           |
| `created_at`  | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —           |
| `updated_at`  | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —           |

---

# 14. `orders`

## 14.1 Purpose

Stores marketplace orders created by users.

Orders are historical business records and should be preserved even when a user account becomes inactive.

---

## 14.2 Columns

| Column         | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints     |
| -------------- | --------------- | ---------------------- | -------- | --------- | --------------- |
| `id`           | `UUID`          | `UUID`                 | No       | generated | PK              |
| `user_id`      | `UUID`          | `UUID`                 | No       | —         | FK → `users.id` |
| `status`       | `VARCHAR(30)`   | Enum / `str`           | No       | `pending` | CHECK           |
| `total_amount` | `NUMERIC(12,2)` | `Decimal`              | No       | —         | >= 0            |
| `created_at`   | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —               |
| `updated_at`   | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —               |

---

## 14.3 Order Status

The current API specification defines:

```text
pending
completed
cancelled
```

The database should prevent unsupported values.

Conceptual constraint:

```sql
CHECK (
    status IN (
        'pending',
        'completed',
        'cancelled'
    )
)
```

---

## 14.4 Order Ownership

```text
orders.user_id → users.id
```

A user can retrieve only their own orders through normal user APIs.

Administrators may access orders according to the administrative authorization policy.

---

# 15. `order_items`

## 15.1 Purpose

Stores individual products included in an order.

---

## 15.2 Columns

| Column       | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints        |
| ------------ | --------------- | ---------------------- | -------- | --------- | ------------------ |
| `id`         | `UUID`          | `UUID`                 | No       | generated | PK                 |
| `order_id`   | `UUID`          | `UUID`                 | No       | —         | FK → `orders.id`   |
| `product_id` | `UUID`          | `UUID`                 | No       | —         | FK → `products.id` |
| `quantity`   | `INTEGER`       | `int`                  | No       | —         | > 0                |
| `unit_price` | `NUMERIC(12,2)` | `Decimal`              | No       | —         | >= 0               |
| `subtotal`   | `NUMERIC(12,2)` | `Decimal`              | No       | —         | >= 0               |

---

## 15.3 Historical Price Rule

`unit_price` should represent the product price at the time of purchase.

Do not calculate historical order values using the current `products.price`.

Example:

```text
Product current price:
$15

Historical order:
unit_price = $10
quantity = 2

subtotal = $20
```

The historical order must remain `$20` even if the current product price changes to `$15`.

---

## 15.4 Quantity

Quantity must be greater than zero.

```text
quantity > 0
```

---

# 16. `posts`

## 16.1 Purpose

Stores community posts created by users.

---

## 16.2 Columns

| Column         | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints     |
| -------------- | --------------- | ---------------------- | -------- | --------- | --------------- |
| `id`           | `UUID`          | `UUID`                 | No       | generated | PK              |
| `user_id`      | `UUID`          | `UUID`                 | No       | —         | FK → `users.id` |
| `title`        | `VARCHAR(200)`  | `str`                  | No       | —         | —               |
| `content`      | `TEXT`          | `str`                  | No       | —         | —               |
| `is_published` | `BOOLEAN`       | `bool`                 | No       | `true`    | —               |
| `created_at`   | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —               |
| `updated_at`   | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —               |

---

## 16.3 Ownership

```text
posts.user_id → users.id
```

A user may create multiple posts.

---

## 16.4 Content Management

Administrators may moderate community content.

Normal users may modify only their own posts according to the community API rules.

---

# 17. `comments`

## 17.1 Purpose

Stores comments made on community posts.

---

## 17.2 Columns

| Column       | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints     |
| ------------ | --------------- | ---------------------- | -------- | --------- | --------------- |
| `id`         | `UUID`          | `UUID`                 | No       | generated | PK              |
| `post_id`    | `UUID`          | `UUID`                 | No       | —         | FK → `posts.id` |
| `user_id`    | `UUID`          | `UUID`                 | No       | —         | FK → `users.id` |
| `content`    | `TEXT`          | `str`                  | No       | —         | —               |
| `created_at` | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —               |
| `updated_at` | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —               |

---

## 17.3 Relationships

```text
comments.post_id → posts.id

comments.user_id → users.id
```

A comment belongs to:

```text
One Post
One User
```

---

# 18. `admin_audit_logs`

## 18.1 Status

**Future / Recommended**

This table is recommended when administrative auditing becomes a required production feature.

---

## 18.2 Purpose

Records important administrative actions for accountability and operational auditing.

---

## 18.3 Proposed Columns

| Column           | PostgreSQL Type | Python / SQLModel Type | Nullable | Default   | Constraints     |
| ---------------- | --------------- | ---------------------- | -------- | --------- | --------------- |
| `id`             | `UUID`          | `UUID`                 | No       | generated | PK              |
| `admin_user_id`  | `UUID`          | `UUID`                 | No       | —         | FK → `users.id` |
| `target_user_id` | `UUID`          | `UUID`                 | Yes      | `NULL`    | FK → `users.id` |
| `action`         | `VARCHAR(100)`  | `str`                  | No       | —         | —               |
| `old_value`      | `JSONB`         | `dict \| None`         | Yes      | `NULL`    | —               |
| `new_value`      | `JSONB`         | `dict \| None`         | Yes      | `NULL`    | —               |
| `created_at`     | `TIMESTAMPTZ`   | `datetime`             | No       | UTC now   | —               |

---

## 18.4 Example Actions

```text
ADMIN_USER_DEACTIVATED
ADMIN_USER_REACTIVATED
ADMIN_ROLE_CHANGED
ADMIN_USER_VERIFIED
ADMIN_USER_HARD_DELETED
```

---

# 19. Foreign Key Summary

The main foreign key relationships are:

| Child Table                  | Column           | Parent Table | Parent Column |
| ---------------------------- | ---------------- | ------------ | ------------- |
| `gardens`                    | `user_id`        | `users`      | `id`          |
| `plants`                     | `garden_id`      | `gardens`    | `id`          |
| `plant_health_records`       | `plant_id`       | `plants`     | `id`          |
| `plant_environment_records`  | `plant_id`       | `plants`     | `id`          |
| `care_reminders`             | `plant_id`       | `plants`     | `id`          |
| `fertilizer_recommendations` | `plant_id`       | `plants`     | `id`          |
| `products`                   | `category_id`    | `categories` | `id`          |
| `orders`                     | `user_id`        | `users`      | `id`          |
| `order_items`                | `order_id`       | `orders`     | `id`          |
| `order_items`                | `product_id`     | `products`   | `id`          |
| `posts`                      | `user_id`        | `users`      | `id`          |
| `comments`                   | `post_id`        | `posts`      | `id`          |
| `comments`                   | `user_id`        | `users`      | `id`          |
| `admin_audit_logs`           | `admin_user_id`  | `users`      | `id`          |
| `admin_audit_logs`           | `target_user_id` | `users`      | `id`          |

---

# 20. Common Constraint Rules

The following rules should be represented at the database level where appropriate.

## Required fields

Required business fields should be:

```text
NOT NULL
```

Examples:

```text
users.email
users.hashed_password
gardens.user_id
plants.garden_id
orders.user_id
orders.status
```

---

## Unique values

Values that must be globally unique should use a database unique constraint.

Example:

```text
users.email
categories.name
```

The exact uniqueness rules for categories and other entities should be confirmed before migration.

---

## Non-negative values

Monetary and quantity fields should reject invalid negative values.

Examples:

```text
products.price >= 0
products.stock_quantity >= 0
orders.total_amount >= 0
order_items.quantity > 0
order_items.unit_price >= 0
```

---

# 21. Soft Deletion

Soft deletion is currently required for users.

The preferred implementation is:

```text
users.is_active = false
```

rather than:

```sql
DELETE FROM users;
```

The application should treat inactive users as unavailable for normal authentication and user-facing operations.

Historical data should remain available where required.

---

# 22. Hard Deletion

Hard deletion should not be the default behavior.

It may be used for:

* GDPR-related data deletion
* Test account cleanup
* Controlled administrative maintenance

Before performing a hard delete, the application must understand the foreign-key dependencies.

Hard deletion must be covered by integration tests.

---

# 23. Database vs Application Validation

Validation should exist at the correct layer.

### Application validation

Use Pydantic/SQLModel validation for:

```text
String length
Input formatting
Request structure
Enum validation
User-facing validation errors
```

### Database validation

Use PostgreSQL constraints for:

```text
Primary keys
Foreign keys
Unique values
NOT NULL
Non-negative numeric values
Critical state constraints
```

Example:

```text
API request
     ↓
Pydantic validation
     ↓
Service business rules
     ↓
Repository
     ↓
PostgreSQL constraints
```

Application validation should improve developer/user experience.

Database constraints provide the final structural protection.

---

# 24. Transaction Boundaries

Operations involving multiple related database changes should execute within an appropriate transaction.

Example:

```text
Create Order
    │
    ├── Create Order
    ├── Create Order Items
    ├── Calculate totals
    └── Update inventory
```

These operations should not leave the database partially updated if one operation fails.

The service layer should define the business transaction boundary.

---

# 25. Schema Implementation Mapping

Each documented table should eventually map to a SQLModel table model.

Example:

```python
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(...)
    email: str = Field(...)
    hashed_password: str = Field(...)
    ...
```

The SQLModel model should implement the specification rather than becoming the specification itself.

The documentation explains **why the field exists and what rules apply**.

The model implements those rules.

---

# 26. Alembic Migration Requirement

Every schema change must be represented by an Alembic migration.

Examples:

```text
Create users table
        ↓
Alembic migration

Add avatar_url
        ↓
Alembic migration

Add user role
        ↓
Alembic migration
```

Do not rely on:

```text
SQLModel.metadata.create_all()
```

for production schema management.

Alembic is the schema migration mechanism for Plantive.

---

# 27. Implementation Status

At the current design stage:

### Ready for detailed implementation

```text
users
gardens
plants
orders
order_items
products
categories
posts
comments
```

### Requires additional domain decisions

```text
plant_health_records
plant_environment_records
care_reminders
fertilizer_recommendations
services
```

### Future

```text
admin_audit_logs
```

The fields marked **Proposed** should be reviewed before generating their Alembic migrations.

---

# 28. Design Rule for Future Tables

Every new Plantive table should be documented using the following structure:

```text
Table Name
    ↓
Purpose
    ↓
Columns
    ↓
Primary Key
    ↓
Foreign Keys
    ↓
Unique Constraints
    ↓
Check Constraints
    ↓
Indexes
    ↓
Ownership
    ↓
Deletion Policy
    ↓
Business Rules
    ↓
Migration
    ↓
Tests
```

This ensures that database design remains intentional and reviewable as Plantive grows.

---

# 29. Final Database Design Principle

The Plantive database should be designed around **business entities and relationships**, not around individual API endpoints.

For example:

```text
API:
GET /api/v1/users/me/orders
```

does not require a special `user_orders` table.

Instead, the API uses the existing relationship:

```text
users
  │
  └──< orders
```

The API, service, and repository layers query the database according to that relationship.

This keeps the database normalized, reusable, and independent from individual HTTP endpoints.

---

# 30. Related Documentation

This document should be read together with:

```text
docs/
├── architecture/
│   └── architecture.md
│
└── database/
    ├── 01-database-overview.md
    ├── 02-database-schema.md
    ├── 03-table-specifications.md
    ├── 04-relationships-and-integrity.md
    ├── 05-indexes-and-query-strategy.md
    └── 06-migrations-and-seeding.md
```

The recommended next document is:

```text
04-relationships-and-integrity.md
```

That document should define the **exact foreign-key behavior (`CASCADE`, `RESTRICT`, `SET NULL`), ownership rules, deletion policies, and integrity rules** for these tables before you start writing your SQLModel models and Alembic migrations.
