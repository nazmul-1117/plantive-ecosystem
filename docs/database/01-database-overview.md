# Plantive Database Overview

**Document:** `01-database-overview.md`\
**Project:** Plantive — Your Smart Gardening Tool\
**Database:** PostgreSQL\
**ORM:** SQLModel\
**Migration Tool:** Alembic\
**Database Driver:** asyncpg\
**Application Framework:** FastAPI\
**Status:** Design Specification\
**Version:** 1.0

---

# 1. Purpose

This document provides a high-level overview of the Plantive database architecture.

It explains:

* Why PostgreSQL is used
* How the database fits into the FastAPI architecture
* The major database domains
* Database design principles
* Entity ownership
* Relationships at a high level
* Data integrity strategy
* Migration strategy
* Transaction strategy
* Soft deletion strategy
* Database responsibilities vs application responsibilities

Detailed table definitions are documented separately in:

```text
docs/
└── database/
    ├── 01-database-overview.md
    ├── 02-database-schema.md
    ├── 03-table-specifications.md
    ├── 04-relationships-and-integrity.md
    ├── 05-indexes-and-query-strategy.md
    └── 06-migrations-and-seeding.md
```

---

# 2. Database Role in Plantive

The database is the persistent storage layer of Plantive.

It stores the application's long-lived business data, including:

* User accounts
* User profiles
* Gardens
* Plants
* Plant health information
* Environmental observations
* Care reminders
* Marketplace products
* Orders
* Community posts
* Comments
* Administrative information

The database does **not** contain every piece of application state.

For example:

```text
PostgreSQL
    ↓
Persistent business data

Redis
    ↓
Short-lived / high-speed application state

Object Storage
    ↓
Images and uploaded files
```

This separation prevents PostgreSQL from becoming responsible for data that is better handled by specialized systems.

---

# 3. Database Technology Stack

Plantive uses the following database-related technologies.

| Technology | Purpose                                                   |
| ---------- | --------------------------------------------------------- |
| PostgreSQL | Primary relational database                               |
| SQLModel   | Python ORM / data modeling                                |
| Alembic    | Database schema migrations                                |
| asyncpg    | Asynchronous PostgreSQL driver                            |
| FastAPI    | Application/API layer                                     |
| Redis      | Cache, rate limiting, refresh-token state, temporary data |

---

# 4. Why PostgreSQL?

PostgreSQL is the primary database for Plantive because the application contains strongly related business entities.

For example:

```text
User
 │
 ├── Garden
 │     │
 │     └── Plant
 │
 ├── Order
 │     │
 │     └── Order Item
 │             │
 │             └── Product
 │
 └── Post
       │
       └── Comment
```

These relationships benefit from relational database features such as:

* Foreign keys
* Transactions
* Unique constraints
* Check constraints
* Indexes
* Strong consistency
* Reliable concurrent writes
* Aggregation queries

PostgreSQL is therefore a good fit for Plantive's core business data.

---

# 5. Database Architecture

The database is accessed through the application's repository layer.

The intended architecture is:

```text
                    HTTP Request
                         │
                         ▼
                    Middleware
                         │
                         ▼
                       Router
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
                     SQLModel
                         │
                         ▼
                    PostgreSQL
```

Other infrastructure services may be accessed separately:

```text
                         Service
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
          Repository      Redis     File Storage
                │
                ▼
           PostgreSQL
```

---

# 6. Database Layer Responsibilities

The database layer is responsible for persistent data integrity.

It should handle:

* Data persistence
* Relationships
* Foreign keys
* Unique constraints
* Required fields
* Database-level validation
* Transactions
* Indexes
* Referential integrity

It should **not** contain HTTP-specific concerns.

For example, the database should not know about:

```text
HTTP 401
HTTP 403
FastAPI dependencies
JWT tokens
Request objects
UploadFile
API response envelopes
```

Those belong to higher application layers.

---

# 7. Database Domains

Plantive's database is organized around several business domains.

```text
Plantive Database
│
├── Identity & Access
│   └── Users
│
├── Gardening
│   ├── Gardens
│   ├── Plants
│   ├── Health Records
│   ├── Environment Records
│   ├── Care Reminders
│   └── Fertilizer Recommendations
│
├── Marketplace
│   ├── Categories
│   ├── Products
│   ├── Services
│   ├── Orders
│   └── Order Items
│
├── Community
│   ├── Posts
│   └── Comments
│
└── Administration
    └── Audit Logs
```

---

# 8. Identity Domain

The identity domain contains user account information.

Primary entity:

```text
users
```

Users are the primary owners of many resources within Plantive.

High-level relationship:

```text
User
 │
 ├──< Gardens
 ├──< Orders
 ├──< Posts
 └──< Comments
```

The user table also contains authorization-related account state such as:

```text
role
is_active
is_verified
```

Authentication credentials are represented by a password hash rather than a plaintext password.

---

# 9. Gardening Domain

The gardening domain represents the core purpose of Plantive.

The primary relationship is:

```text
User
 │
 └──< Garden
          │
          └──< Plant
```

Additional plant-related data may be associated with a plant:

```text
Plant
 │
 ├──< Health Records
 ├──< Environment Records
 ├──< Care Reminders
 └──< Fertilizer Recommendations
```

This structure allows Plantive to maintain both current plant information and historical observations.

---

# 10. Marketplace Domain

The marketplace domain handles products, services, and orders.

The high-level relationship is:

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

An order stores historical purchase information.

Order items should preserve the price at the time of purchase rather than relying on the current product price.

Example:

```text
Product current price = $15

Historical Order Item:
quantity   = 2
unit_price = $10
subtotal   = $20
```

The historical order must remain valid even after the product price changes.

---

# 11. Community Domain

The community domain allows users to interact through posts and comments.

High-level relationship:

```text
User
 │
 └──< Post
          │
          └──< Comment
                   │
                   └── User
```

A post belongs to a user.

A comment belongs to both:

```text
Post
User
```

Community data may be moderated by administrators.

---

# 12. Administration Domain

Administrative functionality operates primarily on existing business entities.

For example:

```text
Admin
 │
 ├── Manage Users
 ├── Manage Products
 ├── Manage Services
 ├── Manage Categories
 ├── Moderate Posts
 └── View Analytics
```

Administrative authorization is handled by the application layer.

The database supports this functionality through:

* User roles
* Entity relationships
* Status fields
* Optional audit records

A future `admin_audit_logs` table may be introduced to record important administrative actions.

---

# 13. Entity Ownership

Ownership is an important part of Plantive's data model.

A resource should be traceable to its owner.

For example:

```text
Plant
 ↓
Garden
 ↓
User
```

Therefore, when a user requests a plant:

```text
GET /api/v1/plants/{plant_id}
```

the application must not simply check whether the plant exists.

It must also verify that the plant belongs to the authenticated user.

Conceptually:

```text
Authenticated User
        │
        ▼
      Garden
        │
        ▼
       Plant
```

This ownership check belongs primarily to the service/business-authorization layer.

The database provides the relationships required to perform the check.

---

# 14. Database Normalization

Plantive follows relational database normalization principles.

The goal is to avoid unnecessary duplication of business data.

For example, an order should not repeatedly store the complete product information for every item.

Instead:

```text
orders
   │
   └──< order_items
             │
             └── product_id → products
```

However, historical values that must remain unchanged should be copied intentionally.

For example:

```text
order_items.unit_price
```

stores the historical purchase price.

This is not considered an accidental duplication because it preserves historical business information.

---

# 15. Primary Key Strategy

Plantive uses UUIDs as primary keys for major entities.

Example:

```text
123e4567-e89b-12d3-a456-426614174000
```

Benefits include:

* Low predictability
* Safe public identifiers
* Good distributed-system compatibility
* No dependence on sequential IDs
* Easier future service separation

The database schema should consistently use UUIDs for entities that are exposed through the API.

---

# 16. Foreign Key Strategy

Foreign keys enforce relationships between database entities.

Example:

```text
gardens.user_id
        │
        ▼
users.id
```

Another example:

```text
plants.garden_id
        │
        ▼
gardens.id
```

This prevents orphaned records and protects referential integrity.

Foreign-key deletion behavior must be explicitly defined.

Detailed behavior is documented in:

```text
04-relationships-and-integrity.md
```

---

# 17. Timestamp Strategy

Persistent entities should normally contain:

```text
created_at
updated_at
```

Historical/event records may additionally use:

```text
recorded_at
```

All timestamps should use UTC.

Recommended PostgreSQL type:

```text
TIMESTAMPTZ
```

Conceptually:

```text
created_at → when the record was created
updated_at → when the record was last modified
recorded_at → when an observation/event occurred
```

Timestamps should not be stored as arbitrary local-time strings.

---

# 18. Monetary Data

Marketplace monetary values should use exact decimal storage.

Recommended PostgreSQL type:

```text
NUMERIC(12,2)
```

Examples:

```text
products.price
services.price
orders.total_amount
order_items.unit_price
order_items.subtotal
```

Floating-point types should not be used for financial amounts.

---

# 19. Soft Deletion Strategy

Plantive uses soft deletion where historical relationships need to remain intact.

The primary example is users.

Instead of:

```sql
DELETE FROM users;
```

normal account deletion performs:

```text
is_active = false
```

The user record remains in PostgreSQL.

This helps preserve relationships with:

```text
Gardens
Orders
Posts
Comments
Historical transactions
```

Soft deletion is therefore a business rule, not simply a database implementation detail.

---

# 20. Hard Deletion

Physical deletion is an exceptional operation.

Hard deletion may be used for:

* GDPR-related deletion
* Test data cleanup
* Controlled administrative maintenance

It must not be used casually because related records may reference the entity.

Before implementing hard deletion, the project's foreign-key policies must be explicitly defined.

---

# 21. PostgreSQL Constraints

Plantive should use database constraints wherever a rule is fundamental to data integrity.

Examples include:

### Primary key

```text
users.id
```

### Unique constraint

```text
users.email
```

### Foreign key

```text
gardens.user_id → users.id
```

### NOT NULL

```text
users.email
users.hashed_password
```

### Check constraint

```text
products.price >= 0
```

### Enum/state constraint

```text
orders.status IN (
    'pending',
    'completed',
    'cancelled'
)
```

The application should not rely entirely on Python validation for critical database integrity.

---

# 22. Application Validation vs Database Integrity

Validation exists at multiple layers.

```text
HTTP Request
     │
     ▼
Pydantic / SQLModel Validation
     │
     ▼
Service Business Rules
     │
     ▼
Repository
     │
     ▼
PostgreSQL Constraints
```

### Pydantic / SQLModel

Responsible for:

* Request structure
* Type validation
* String length
* Input formatting
* API-level validation

### Service

Responsible for:

* Business rules
* Authorization decisions
* Ownership checks
* Workflows
* Cross-entity rules

### PostgreSQL

Responsible for:

* Referential integrity
* Uniqueness
* Required data
* Critical numeric constraints
* Persistent state integrity

---

# 23. Transaction Strategy

Transactions are required whenever multiple database operations represent one logical business operation.

Example:

```text
Create Order
    │
    ├── Create order
    ├── Create order items
    ├── Calculate total
    └── Update inventory
```

These operations should be treated as one logical transaction where appropriate.

If an operation fails:

```text
BEGIN
   ↓
operation 1
   ↓
operation 2
   ↓
ERROR
   ↓
ROLLBACK
```

The database should not be left in a partially updated state.

---

# 24. SQLModel Role

SQLModel provides the Python representation of database entities.

Example:

```python
class User(SQLModel, table=True):
    ...
```

SQLModel is responsible for mapping Python objects to database tables.

However, the SQLModel class should not become the only source of database design knowledge.

The documentation defines:

```text
What the data means
What constraints exist
Why the relationship exists
What the business rules are
```

The SQLModel model implements that design.

---

# 25. Alembic Role

Alembic manages database schema evolution.

The expected flow is:

```text
Change Database Design
        │
        ▼
Update SQLModel Models
        │
        ▼
Create Alembic Migration
        │
        ▼
Review Migration
        │
        ▼
Apply Migration
        │
        ▼
PostgreSQL
```

Production database changes should be delivered through Alembic migrations.

The application should not depend on automatically creating production tables at startup.

---

# 26. Redis vs PostgreSQL

Redis is not a replacement for PostgreSQL.

Plantive uses the two systems for different purposes.

| PostgreSQL | Redis                              |
| ---------- | ---------------------------------- |
| Users      | Refresh-token state                |
| Gardens    | Rate limiting                      |
| Plants     | Cache                              |
| Orders     | Temporary data                     |
| Products   | Short-lived state                  |
| Posts      | OTP / verification state if needed |
| Comments   | Frequently accessed cached data    |

The general rule is:

```text
If the data must survive application restarts
and represents core business information:
        → PostgreSQL

If the data is temporary, cached, or high-speed state:
        → Redis
```

---

# 27. File Storage vs PostgreSQL

User-uploaded files such as avatars should not normally be stored directly inside PostgreSQL.

Recommended architecture:

```text
Client
  │
  ▼
FastAPI
  │
  ├──────────────► Object Storage
  │                  │
  │                  └── avatar.webp
  │
  └──────────────► PostgreSQL
                       │
                       └── avatar_url
```

PostgreSQL stores the reference to the file.

The binary file is stored separately.

---

# 28. Indexing Philosophy

Indexes should be added based on actual query patterns.

Important candidates include:

```text
users.email
users.role
users.is_active

gardens.user_id

plants.garden_id

orders.user_id
orders.status

order_items.order_id
order_items.product_id

posts.user_id

comments.post_id
comments.user_id
```

Indexes should not be created blindly on every column.

Indexes improve reads but introduce:

* Storage cost
* Write overhead
* Maintenance overhead

Detailed index decisions belong in:

```text
05-indexes-and-query-strategy.md
```

---

# 29. Pagination Strategy

Large collections should be paginated at the database/query layer.

Example:

```text
GET /api/v1/admin/users?page=1&page_size=20
```

The API response may contain:

```json
{
  "page": 1,
  "page_size": 20,
  "total_items": 142,
  "total_pages": 8
}
```

The repository layer should perform the appropriate:

```text
COUNT
LIMIT
OFFSET
```

or another documented pagination strategy.

Pagination is an API concern implemented using database query capabilities.

---

# 30. Database Security Principles

The application must follow least-privilege principles.

The FastAPI application should connect using a database account that has only the permissions required by the application.

Production database credentials must not be committed to Git.

Credentials should be provided through environment configuration.

Example:

```text
DATABASE_URL
```

should be loaded through the application's settings system.

Never hard-code:

```text
database password
database credentials
production connection strings
```

in source code.

---

# 31. Development Database

During development, the developer may use a local PostgreSQL instance.

The development environment should be isolated from production.

Example:

```text
Development
    ↓
Local PostgreSQL
    ↓
plantive_dev
```

Production:

```text
Production
    ↓
Managed PostgreSQL / Production PostgreSQL
    ↓
plantive
```

The two environments must never accidentally share credentials or databases.

---

# 32. Testing Database

Automated tests should use a dedicated test database.

Example:

```text
plantive_test
```

Tests should not execute destructive operations against development or production databases.

The test database should be disposable and reproducible.

---

# 33. Database Environment Separation

Plantive should conceptually maintain:

```text
┌─────────────────────┐
│ Development         │
│ PostgreSQL          │
└─────────────────────┘

┌─────────────────────┐
│ Testing             │
│ PostgreSQL          │
└─────────────────────┘

┌─────────────────────┐
│ Production          │
│ PostgreSQL          │
└─────────────────────┘
```

Each environment should have separate:

* Database
* Credentials
* Connection configuration
* Migration execution process

---

# 34. Database Access Pattern

Application code should not directly execute database queries from controllers.

Avoid:

```text
Router
   ↓
SQL query
```

Preferred:

```text
Router
   ↓
Controller
   ↓
Service
   ↓
Repository
   ↓
Database
```

### Controller

Handles HTTP concerns.

### Service

Handles business logic.

### Repository

Handles persistence/query logic.

### Database

Stores and enforces persistent data.

This separation keeps the codebase easier to test and maintain.

---

# 35. Example Request Flow

Consider:

```text
GET /api/v1/users/me/gardens
```

The expected flow is:

```text
Client
  │
  ▼
FastAPI Router
  │
  ▼
Authentication Dependency
  │
  ▼
Controller
  │
  ▼
Garden Service
  │
  ▼
Garden Repository
  │
  ▼
PostgreSQL
```

The repository performs the database query.

The service ensures the query is being performed for the authenticated user.

The controller converts the result into the API response schema.

---

# 36. Database Documentation Responsibilities

Database documentation should answer:

```text
What tables exist?
        ↓
What does each table represent?
        ↓
What relationships exist?
        ↓
What constraints exist?
        ↓
Who owns the data?
        ↓
How is deletion handled?
        ↓
How are migrations managed?
        ↓
How is the database tested?
```

The documentation should not become a copy of the SQLModel source code.

It should explain the design decisions behind the implementation.

---

# 37. Source of Truth

Plantive uses several related sources of truth, each for a different concern.

| Concern                      | Source of Truth        |
| ---------------------------- | ---------------------- |
| API contract                 | API specification      |
| Database design              | Database documentation |
| Database schema history      | Alembic migrations     |
| Python database mapping      | SQLModel models        |
| Business behavior            | Service layer          |
| Authentication/authorization | Security layer         |
| Runtime configuration        | Application settings   |

The database documentation defines the intended database design.

Alembic defines how that design evolves over time.

---

# 38. Database Documentation Structure

The database documentation should be maintained as a small set of focused documents.

Recommended structure:

```text
docs/
└── database/
    │
    ├── 01-database-overview.md
    │
    ├── 02-database-schema.md
    │
    ├── 03-table-specifications.md
    │
    ├── 04-relationships-and-integrity.md
    │
    ├── 05-indexes-and-query-strategy.md
    │
    └── 06-migrations-and-seeding.md
```

Each document has a different responsibility.

### `01-database-overview.md`

High-level database architecture and principles.

### `02-database-schema.md`

Overall schema/entity map.

### `03-table-specifications.md`

Detailed table and column definitions.

### `04-relationships-and-integrity.md`

Foreign keys, ownership, deletion behavior, and integrity rules.

### `05-indexes-and-query-strategy.md`

Indexes, common queries, pagination, and performance considerations.

### `06-migrations-and-seeding.md`

Alembic workflow, migration rules, seed data, and deployment practices.

---

# 39. Design Principles

The Plantive database follows these core principles:

## 39.1 Data Integrity First

Important relationships and constraints should be enforced by PostgreSQL.

## 39.2 Explicit Relationships

Every relationship should have a clear foreign key.

## 39.3 Clear Ownership

User-owned resources must be traceable to the owning user.

## 39.4 Historical Data Preservation

Business history such as orders should remain meaningful even when related current data changes.

## 39.5 Soft Delete Where Appropriate

Entities requiring historical preservation should not be physically deleted by default.

## 39.6 UTC Timestamps

Persistent timestamps should be timezone-aware and stored in UTC.

## 39.7 Exact Monetary Values

Financial values use decimal database types.

## 39.8 Migration-Based Schema Changes

Production schema changes must go through Alembic.

## 39.9 Layered Database Access

Controllers should not directly access PostgreSQL.

## 39.10 Keep Infrastructure Responsibilities Separate

PostgreSQL, Redis, and object storage should each handle the type of data they are designed for.

---

# 40. Current Database Design Scope

The current Plantive database focuses on these core capabilities:

```text
                    Plantive
                       │
       ┌───────────────┼────────────────┐
       │               │                │
       ▼               ▼                ▼
   Identity        Gardening        Marketplace
       │               │                │
     Users          Gardens           Products
                       │              Services
                     Plants             Orders
                       │
              Health / Environment
                       │
                       ▼
                   Reminders

                       │
                       ▼
                   Community
                       │
                 Posts / Comments
```

The database can be expanded later for:

* AI assistant conversation history
* Notifications
* Payment records
* Shipping information
* Product reviews
* Plant disease detection
* Weather history
* User preferences
* Analytics
* Administrative audit logs

These should be added only when their business requirements are defined.

---

# 41. Final Architecture Principle

The Plantive database should remain **boring, predictable, relational, and strongly constrained**.

Complex business behavior should primarily live in the application layers:

```text
Router
   ↓
Controller
   ↓
Service
   ↓
Repository
   ↓
PostgreSQL
```

PostgreSQL should focus on what it does best:

```text
Persist data
Maintain relationships
Protect integrity
Execute queries
Handle transactions
```

FastAPI and the service layer should handle:

```text
HTTP
Authentication
Authorization
Business workflows
Validation
Application behavior
```

Redis should handle:

```text
Caching
Rate limiting
Temporary state
Refresh-token state
```

Object storage should handle:

```text
Images
Uploaded files
Media
```

Keeping these responsibilities separated gives Plantive a clean foundation for learning and eventually evolving toward a production-grade backend.
