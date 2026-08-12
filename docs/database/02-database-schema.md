    ├── 01-database-overview.md
    ├── 02-database-schema.md
    ├── 03-table-specifications.md
    ├── 04-relationships-and-integrity.md
    ├── 05-indexes-and-query-strategy.md
    └── 06-migrations-and-seeding.md


# Plantive Database Schema

**Document:** `02-database-schema.md`
**Project:** Plantive — Your Smart Gardening Tool
**Database:** PostgreSQL
**ORM:** SQLModel
**Migration Tool:** Alembic
**Database Driver:** asyncpg
**Status:** Design Specification
**Version:** 1.0

---

# 1. Purpose

This document defines the high-level database schema for **Plantive — Your Smart Gardening Tool**.

It describes:

* Major database domains
* Core database tables
* Table ownership and responsibilities
* High-level relationships between tables
* Primary domain boundaries
* Data ownership principles
* Soft-deletion strategy
* Database design conventions

This document does **not** define every column, constraint, or index.

Detailed table definitions are documented separately in:

```text
docs/database/03-table-specifications.md
```

---

# 2. Database Technology

Plantive uses PostgreSQL as its primary persistent database.

| Component             | Technology |
| --------------------- | ---------- |
| Database              | PostgreSQL |
| ORM / Model Layer     | SQLModel   |
| SQL Toolkit           | SQLAlchemy |
| Async Driver          | asyncpg    |
| Migration Tool        | Alembic    |
| Application Framework | FastAPI    |
| Cache / Session State | Redis      |

PostgreSQL is the **source of truth for persistent application data**.

Redis is not considered the primary database.

Redis is used for temporary or fast-access data such as:

* Refresh-token/session state
* Rate limiting
* Caching where appropriate
* Other temporary application state

---

# 3. Database Architecture

The application accesses PostgreSQL through the repository layer.

```text
HTTP Request
     │
     ▼
FastAPI Router
     │
     ▼
Controller
     │
     ▼
Service
     │
     ▼
Repository
     │
     ▼
SQLModel / SQLAlchemy
     │
     ▼
asyncpg
     │
     ▼
PostgreSQL
```

The application should not access PostgreSQL directly from controllers.

The recommended responsibility boundary is:

```text
Router
  → HTTP concerns

Controller
  → Request/response coordination

Service
  → Business rules and transactions

Repository
  → Database queries and persistence

PostgreSQL
  → Durable data and relational integrity
```

---

# 4. Database Design Principles

The Plantive database follows these principles.

## 4.1 PostgreSQL as the Source of Truth

Persistent business data must be stored in PostgreSQL.

Examples:

* Users
* Gardens
* Plants
* Orders
* Products
* Posts
* Comments

Redis must not be used as the permanent source of truth for these entities.

---

## 4.2 Relational Integrity

Relationships between entities should be represented using PostgreSQL foreign keys.

For example:

```text
users
  │
  └──< gardens
```

A garden belongs to a user through:

```text
gardens.user_id → users.id
```

Foreign keys prevent invalid references and help maintain database consistency.

---

## 4.3 Domain Separation

Tables are organized according to their business domain.

Plantive currently contains the following major domains:

```text
Identity & Access
Gardening
Marketplace
Community
Administration
```

Each domain owns its relevant entities.

---

## 4.4 Application-Level Business Rules

Some rules belong primarily to the service layer.

Examples:

```text
An administrator cannot demote themselves.
A user can only update their own profile.
A user can only access their own orders.
```

These rules are enforced by the application.

Other structural rules should be enforced by PostgreSQL.

Examples:

```text
email must be unique
foreign key must reference an existing row
required field cannot be NULL
```

The application and database should therefore work together rather than relying entirely on one layer.

---

# 5. Database Domain Overview

The Plantive database is divided into the following domains:

```text
Plantive Database
│
├── Identity & Access
│
├── Gardening
│
├── Marketplace
│
├── Community
│
└── Administration
```

---

# 6. Identity & Access Domain

The Identity & Access domain manages users and authentication-related persistent state.

### Primary tables

```text
users
```

Depending on the final authentication implementation, additional authentication-related tables may be introduced.

For example:

```text
refresh_sessions
```

or another session/token persistence model.

However, short-lived authentication state may also be managed through Redis rather than PostgreSQL.

---

## 6.1 `users`

The `users` table represents an account registered on Plantive.

It stores:

* Identity information
* Login email
* Password hash
* Display name
* Avatar reference
* User role
* Account status
* Verification status
* Creation timestamp
* Modification timestamp

High-level structure:

```text
users
│
├── id
├── email
├── hashed_password
├── full_name
├── avatar_url
├── role
├── is_active
├── is_verified
├── created_at
└── updated_at
```

A user may own or create resources across multiple Plantive domains.

```text
User
│
├── Gardens
├── Orders
├── Posts
├── Comments
└── other user-owned resources
```

---

# 7. Gardening Domain

The Gardening domain contains the core functionality that allows users to manage their gardens and plants.

Primary entities include:

```text
gardens
plants
plant_health_records
plant_environment_records
care_reminders
fertilizer_recommendations
```

The exact table list may evolve as the gardening module is implemented.

---

# 8. `gardens`

A garden represents a personal garden owned by a Plantive user.

High-level relationship:

```text
User
 │
 └──< Gardens
```

Database relationship:

```text
gardens.user_id → users.id
```

A user can have multiple gardens.

```text
User
 │
 ├── Garden A
 ├── Garden B
 └── Garden C
```

A garden acts as a parent container for plants.

```text
Garden
 │
 └──< Plants
```

---

# 9. `plants`

A plant represents a plant being managed by a user inside a garden.

High-level relationship:

```text
User
 │
 └──< Garden
          │
          └──< Plant
```

Database relationship:

```text
plants.garden_id → gardens.id
```

A garden can contain multiple plants.

Example:

```text
Garden: Rooftop Garden
│
├── Tomato
├── Basil
├── Mint
└── Rose
```

The plant entity is expected to contain information required for:

* Plant identification
* Plant care
* Plant status
* Plant health monitoring
* Care scheduling

---

# 10. Plant Health Records

Plant health records represent historical or current health observations for plants.

High-level relationship:

```text
Plant
 │
 └──< Plant Health Records
```

Conceptually:

```text
plants.id
    ↓
plant_health_records.plant_id
```

Multiple health records may exist for a single plant.

Example:

```text
Plant: Tomato
│
├── Health Record — July 01
├── Health Record — July 08
├── Health Record — July 15
└── Health Record — July 22
```

This allows Plantive to maintain historical health information rather than storing only the latest state.

---

# 11. Plant Environment Records

Environment records represent simulated or collected environmental conditions associated with plants or gardens.

Potential data includes:

* Temperature
* Humidity
* Soil moisture
* Light level
* Other environmental measurements

High-level relationship:

```text
Plant
 │
 └──< Environment Records
```

The final ownership model may associate environment data with either:

```text
plant
```

or:

```text
garden
```

depending on the final implementation.

This decision should be finalized before creating the corresponding Alembic migration.

---

# 12. `care_reminders`

Care reminders represent scheduled actions related to plant care.

Examples:

```text
Water tomato
Fertilize basil
Check soil moisture
Move plant to sunlight
```

High-level relationship:

```text
User
 │
 └──< Garden
          │
          └──< Plant
                   │
                   └──< Care Reminder
```

A reminder should belong to the appropriate user-owned gardening resource.

---

# 13. `fertilizer_recommendations`

Fertilizer recommendations contain recommendations generated based on plant requirements.

They may be associated with:

```text
Plant
```

and/or:

```text
User
```

depending on whether recommendations are treated as persistent history or dynamically generated results.

The final persistence strategy should be decided before implementation.

Not every AI-generated result needs to be stored permanently.

---

# 14. Gardening Domain Relationship

The primary gardening structure is:

```text
User
 │
 └──< Garden
          │
          └──< Plant
                   │
                   ├──< Health Record
                   ├──< Environment Record
                   ├──< Care Reminder
                   └──< Fertilizer Recommendation
```

This is the core relationship chain of the Plantive gardening system.

---

# 15. Marketplace Domain

The Marketplace domain manages products, categories, services, and customer orders.

Primary tables include:

```text
categories
products
services
orders
order_items
```

The marketplace structure is conceptually:

```text
Category
 │
 └──< Product

User
 │
 └──< Order
          │
          └──< Order Item
                     │
                     └── Product
```

---

# 16. `categories`

Categories organize marketplace products.

Examples:

```text
Plants
Gardening Tools
Fertilizers
Pots
Seeds
```

High-level relationship:

```text
Category
 │
 └──< Products
```

A category may contain many products.

---

# 17. `products`

Products represent items that can be purchased through the Plantive marketplace.

Examples:

```text
Rose Plant
Organic Fertilizer
Garden Shovel
Plant Pot
```

A product may belong to a category.

```text
Category
 │
 └──< Product
```

Products may later contain additional entities such as:

```text
product_images
product_inventory
product_reviews
```

These should be introduced only when required by the marketplace specification.

---

# 18. `services`

Services represent gardening-related services offered through the marketplace.

Examples:

```text
Garden Maintenance
Plant Consultation
Garden Setup
Landscaping
```

Services are conceptually different from physical products and should therefore remain a separate domain entity unless a future marketplace redesign intentionally unifies them.

---

# 19. `orders`

An order represents a purchase made by a user.

Relationship:

```text
User
 │
 └──< Order
```

Database relationship:

```text
orders.user_id → users.id
```

An order contains one or more order items.

```text
Order
 │
 └──< Order Items
```

Example:

```text
Order #1001
│
├── 2 × Rose Plant
├── 1 × Organic Fertilizer
└── 1 × Garden Shovel
```

Order records are historical business records and should generally be preserved even when the associated user account is deactivated.

---

# 20. `order_items`

An order item represents a specific product included in an order.

Relationship:

```text
Order
 │
 └──< Order Item
          │
          └── Product
```

Conceptually:

```text
orders.id
    ↓
order_items.order_id

products.id
    ↓
order_items.product_id
```

The order item should preserve the relevant purchase-time information.

For example, the purchased price should normally be stored in the order item rather than relying on the product's current price.

This is important because:

```text
Product price today
```

may be different from:

```text
Product price at the time of purchase
```

Historical orders must remain accurate.

---

# 21. Marketplace Domain Relationship

```text
User
 │
 └──< Order
          │
          └──< Order Item
                   │
                   └── Product
                          │
                          └── Category
```

Services are represented separately:

```text
Marketplace
├── Products
│    └── Categories
│
├── Services
│
└── Orders
     └── Order Items
```

---

# 22. Community Domain

The Community domain allows users to share gardening experiences and interact with other users.

Primary tables:

```text
posts
comments
```

Additional interaction tables may include:

```text
post_likes
```

or another interaction model depending on the final community specification.

---

# 23. `posts`

A post represents content published by a user.

Relationship:

```text
User
 │
 └──< Posts
```

Database relationship:

```text
posts.user_id → users.id
```

A post may have many comments.

```text
Post
 │
 └──< Comments
```

---

# 24. `comments`

A comment represents a user's response to a community post.

Relationships:

```text
User
 │
 └──< Comments

Post
 │
 └──< Comments
```

Conceptually:

```text
comments.user_id → users.id
comments.post_id → posts.id
```

Therefore:

```text
User A
   │
   └── Comment
          │
          └── Post B
```

A comment belongs to both:

* The user who created it
* The post it belongs to

---

# 25. Community Domain Relationship

```text
User
 │
 ├──< Post
 │      │
 │      └──< Comment
 │
 └──< Comment
```

This allows Plantive to support:

* User-generated posts
* Comments
* Community discussions
* Gardening experiences
* Future social interactions

---

# 26. Administration Domain

The Administration domain provides operational control over the Plantive platform.

Administrative operations currently operate primarily on existing domain entities.

Examples:

```text
Manage Users
Manage Plants
Manage Products
Manage Services
Manage Categories
Manage Community Content
View Platform Analytics
```

The initial database design does not require a separate table for every administrative operation.

For example:

```text
Admin updates User
```

updates the existing:

```text
users
```

table.

---

# 27. Administrative Audit Logs

A future `admin_audit_logs` table is recommended for production auditing.

Conceptually:

```text
admin_audit_logs
│
├── id
├── admin_user_id
├── target_user_id
├── action
├── old_value
├── new_value
└── created_at
```

Example events:

```text
ADMIN_USER_DEACTIVATED
ADMIN_USER_REACTIVATED
ADMIN_ROLE_CHANGED
ADMIN_USER_VERIFIED
ADMIN_USER_HARD_DELETED
```

This table is not required for the initial User module if auditing is implemented later as a dedicated module.

However, the architecture should leave room for it.

---

# 28. Complete High-Level Schema

The current Plantive database can be represented as:

```text
                                ┌──────────────┐
                                │    USERS     │
                                └──────┬───────┘
                                       │
                 ┌─────────────────────┼─────────────────────┐
                 │                     │                     │
                 ▼                     ▼                     ▼
          ┌────────────┐        ┌────────────┐        ┌────────────┐
          │  GARDENS   │        │   ORDERS   │        │   POSTS    │
          └─────┬──────┘        └─────┬──────┘        └─────┬──────┘
                │                     │                     │
                ▼                     ▼                     ▼
          ┌────────────┐        ┌────────────┐        ┌────────────┐
          │   PLANTS   │        │ ORDER_ITEMS│        │  COMMENTS  │
          └─────┬──────┘        └─────┬──────┘        └────────────┘
                │                     │
       ┌────────┼────────┐            ▼
       │        │        │       ┌────────────┐
       ▼        ▼        ▼       │  PRODUCTS  │
    HEALTH   ENVIRONMENT CARE     └─────┬──────┘
    RECORDS   RECORDS    REMINDERS      │
                                        ▼
                                  ┌────────────┐
                                  │ CATEGORIES │
                                  └────────────┘

                         ┌────────────┐
                         │  SERVICES  │
                         └────────────┘
```

---

# 29. Entity Inventory

The initial database entity inventory is:

| Domain         | Table                        | Primary Responsibility       |
| -------------- | ---------------------------- | ---------------------------- |
| Identity       | `users`                      | User accounts                |
| Gardening      | `gardens`                    | User gardens                 |
| Gardening      | `plants`                     | Managed plants               |
| Gardening      | `plant_health_records`       | Plant health history         |
| Gardening      | `plant_environment_records`  | Environmental observations   |
| Gardening      | `care_reminders`             | Plant care reminders         |
| Gardening      | `fertilizer_recommendations` | Fertilizer recommendations   |
| Marketplace    | `categories`                 | Product categorization       |
| Marketplace    | `products`                   | Marketplace products         |
| Marketplace    | `services`                   | Gardening services           |
| Marketplace    | `orders`                     | Customer purchases           |
| Marketplace    | `order_items`                | Products within orders       |
| Community      | `posts`                      | User-generated posts         |
| Community      | `comments`                   | Post comments                |
| Administration | `admin_audit_logs`           | Administrative audit history |

Some entities are intentionally marked as **future/conditional** and should not be created until their corresponding module specification is finalized.

---

# 30. Primary Relationship Map

The most important relationships are:

```text
users
 │
 ├──< gardens
 │      │
 │      └──< plants
 │             │
 │             ├──< plant_health_records
 │             ├──< plant_environment_records
 │             ├──< care_reminders
 │             └──< fertilizer_recommendations
 │
 ├──< orders
 │      │
 │      └──< order_items
 │               │
 │               └── products
 │                      │
 │                      └── categories
 │
 ├──< posts
 │      │
 │      └──< comments
 │
 └──< comments
```

---

# 31. Cardinality Rules

The current design follows these primary cardinalities:

| Relationship               | Cardinality |
| -------------------------- | ----------- |
| User → Garden              | One-to-Many |
| Garden → Plant             | One-to-Many |
| Plant → Health Record      | One-to-Many |
| Plant → Environment Record | One-to-Many |
| Plant → Care Reminder      | One-to-Many |
| User → Order               | One-to-Many |
| Order → Order Item         | One-to-Many |
| Product → Order Item       | One-to-Many |
| Category → Product         | One-to-Many |
| User → Post                | One-to-Many |
| Post → Comment             | One-to-Many |
| User → Comment             | One-to-Many |

Many-to-many relationships, if introduced later, should normally be represented using explicit association tables.

---

# 32. User Ownership Model

A major principle in Plantive is **resource ownership**.

User-owned resources should have an explicit ownership path.

Examples:

```text
Garden
    → user_id

Order
    → user_id

Post
    → user_id
```

For nested resources:

```text
Plant
    → garden_id
    → Garden → user_id
```

This allows the application to determine:

```text
Does this resource belong to the authenticated user?
```

before allowing access.

---

# 33. Data Access Boundary

The database schema supports the following security model:

```text
Authenticated User
       │
       ▼
current_user.id
       │
       ▼
Owned Resource Query
       │
       ▼
PostgreSQL
```

For example:

```sql
SELECT *
FROM orders
WHERE user_id = :current_user_id;
```

The application must not trust a client-provided `user_id` for `/users/me` operations.

---

# 34. Soft Deletion Strategy

Plantive uses soft deletion for user accounts.

For a normal user deletion:

```text
users.is_active = false
```

The user row remains in PostgreSQL.

This is important because other entities may reference the user:

```text
users
 ├── orders
 ├── posts
 ├── comments
 ├── gardens
 └── other historical data
```

Soft deletion preserves these relationships.

---

# 35. Hard Deletion Strategy

Hard deletion is exceptional.

It should only be performed after evaluating all dependent records.

Conceptually:

```text
Hard Delete User
       │
       ├── Check dependencies
       │
       ├── Apply FK policies
       │
       ├── Remove permitted records
       │
       └── Delete user
```

Hard deletion must never be introduced without corresponding database integration tests.

---

# 36. Timestamp Convention

Persistent entities should generally include:

```text
created_at
updated_at
```

where appropriate.

Timestamps should use UTC.

Recommended PostgreSQL type:

```text
TIMESTAMPTZ
```

Application-level datetime values should be timezone-aware.

Example:

```text
2026-08-11T10:30:00Z
```

---

# 37. Primary Key Convention

Plantive uses UUID-based identifiers for primary entities.

Example:

```text
123e4567-e89b-12d3-a456-426614174000
```

Benefits include:

* Reduced predictability
* Better suitability for distributed systems
* Avoiding sequential public identifiers
* Consistent API resource identification

UUIDs do not replace authorization.

Even though a UUID is difficult to guess, ownership and RBAC checks are still mandatory.

---

# 38. Naming Conventions

Database naming follows snake_case.

Examples:

```text
user_id
created_at
updated_at
is_active
is_verified
order_items
plant_health_records
```

Table names should generally be plural:

```text
users
gardens
plants
orders
posts
comments
```

Foreign keys should follow:

```text
<referenced_entity>_id
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

# 39. Schema Evolution

The database schema is managed through Alembic migrations.

The expected workflow is:

```text
SQLModel Model Change
        │
        ▼
Alembic Migration
        │
        ▼
Migration Review
        │
        ▼
PostgreSQL
```

The database schema must not be manually modified in production without a corresponding migration.

Alembic migration files are part of the project's version-controlled source code.

---

# 40. Schema vs. Table Specification

This document intentionally provides a high-level view.

The documentation hierarchy is:

```text
02-database-schema.md
        │
        └── What entities exist?
              │
              ▼
03-table-specifications.md
        │
        └── What columns and constraints exist?
              │
              ▼
04-relationships-and-integrity.md
        │
        └── How are entities connected?
              │
              ▼
05-indexes-and-query-strategy.md
        │
        └── How is the database optimized?
              │
              ▼
06-migrations-and-seeding.md
        │
        └── How does the schema evolve?
```

This separation prevents one documentation file from becoming unnecessarily large.

---

# 41. Current Schema Status

The following entities are part of the planned Plantive database architecture:

### Core

```text
users
```

### Gardening

```text
gardens
plants
plant_health_records
plant_environment_records
care_reminders
fertilizer_recommendations
```

### Marketplace

```text
categories
products
services
orders
order_items
```

### Community

```text
posts
comments
```

### Administration

```text
admin_audit_logs
```

The exact columns, constraints, indexes, foreign-key actions, and implementation details must be finalized in their respective database specifications before production migration.

---

# 42. Implementation Rule

A database table should not be created merely because it appears in this high-level document.

Before creating a production table:

```text
High-Level Schema
      ↓
Table Specification
      ↓
Relationship Specification
      ↓
Index / Query Review
      ↓
SQLModel Model
      ↓
Alembic Migration
      ↓
Integration Tests
```

This ensures that the database design is intentional rather than being generated accidentally from Python models.
