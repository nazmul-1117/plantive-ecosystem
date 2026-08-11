# Plantive — User & Profile Management

## FastAPI Engineering Specification

> **Module:** User & Profile Management
> **API Version:** `v1`
> **Base Paths:** `/api/v1/users`, `/api/v1/admin/users`
> **Database:** PostgreSQL
> **ORM:** SQLModel
> **Migrations:** Alembic
> **Cache / Session State:** Redis
> **Status:** Production Specification

---

# 1. Module Overview

The User & Profile Management module is responsible for:

* Authenticated user profile retrieval
* Authenticated user profile updates
* User self-deactivation
* Avatar upload and removal
* User garden summaries
* User order history
* User community-post history
* Administrative user listing
* Administrative user inspection
* Administrative user status/role management
* Administrative user deactivation
* Controlled hard deletion
* Admin Role-Based Access Control (RBAC)

This module builds directly on the Authentication module.

The Authentication module establishes **who the user is**.

This module determines:

```text
What can this user access?
What user data can they modify?
Can this user perform administrative operations?
```

---

# 2. Architectural Principles

## 2.1 Self vs. Admin Context

User self-management endpoints use:

```text
/api/v1/users/me
```

The target user ID is derived exclusively from the validated Access JWT.

The client must not provide its own user ID for self-management operations.

```text
JWT
 ↓
get_current_user()
 ↓
current_user.id
 ↓
Service
```

This prevents a client from attempting:

```text
/users/me → another user's ID
```

---

## 2.2 Admin Context

Administrative endpoints use:

```text
/api/v1/admin/users
```

and require:

```python
Depends(require_role("admin"))
```

The target user ID is explicitly provided in the URL:

```text
/api/v1/admin/users/{id}
```

The authenticated administrator and target user must be treated as two separate identities.

```text
Authenticated Admin
        │
        ├── current_admin.id
        │
        ▼
   Authorization
        │
        ▼
Target User
    {id}
```

---

## 2.3 Soft Deletion

Normal user deletion is implemented as deactivation:

```python
user.is_active = False
```

The database row remains available.

This preserves historical relationships such as:

* Orders
* Transactions
* Community posts
* Comments
* Gardens
* Plants
* Other historical records

The default deletion strategy is therefore:

```text
DELETE request
      ↓
is_active = False
      ↓
revoke active sessions
      ↓
preserve database record
```

---

## 2.4 Hard Deletion

Hard deletion is exceptional and should not be treated as the normal application workflow.

```text
hard_delete=true
```

should only be permitted for explicitly approved cases such as:

* GDPR/data-erasure workflows
* Test-account cleanup
* Controlled administrative maintenance

Before implementing hard deletion, all relevant PostgreSQL foreign-key relationships and deletion policies must be reviewed.

A hard delete must never accidentally destroy unrelated historical records.

---

# 3. Route Map

| Method   | Endpoint                   | Authentication | Purpose                |
| -------- | -------------------------- | -------------- | ---------------------- |
| `GET`    | `/api/v1/users/me`         | User           | Retrieve own profile   |
| `PATCH`  | `/api/v1/users/me`         | User           | Update own profile     |
| `DELETE` | `/api/v1/users/me`         | User           | Deactivate own account |
| `POST`   | `/api/v1/users/me/avatar`  | User           | Upload/replace avatar  |
| `DELETE` | `/api/v1/users/me/avatar`  | User           | Remove avatar          |
| `GET`    | `/api/v1/users/me/gardens` | User           | List user's gardens    |
| `GET`    | `/api/v1/users/me/orders`  | User           | List user's orders     |
| `GET`    | `/api/v1/users/me/posts`   | User           | List user's posts      |
| `GET`    | `/api/v1/admin/users`      | Admin          | List users             |
| `GET`    | `/api/v1/admin/users/{id}` | Admin          | Retrieve user          |
| `PATCH`  | `/api/v1/admin/users/{id}` | Admin          | Modify user controls   |
| `DELETE` | `/api/v1/admin/users/{id}` | Admin          | Deactivate/delete user |

---

# 4. Recommended Module Structure

For the current Plantive architecture:

```text
app/
├── controllers/
│   ├── user_controller.py
│   └── admin_user_controller.py
│
├── dependencies/
│   ├── auth.py
│   └── pagination.py
│
├── exceptions/
│   ├── user.py
│   └── authorization.py
│
├── models/
│   └── user.py
│
├── repositories/
│   └── user_repository.py
│
├── routers/
│   ├── users.py
│   └── admin_users.py
│
├── schemas/
│   ├── user.py
│   ├── admin_user.py
│   └── pagination.py
│
├── services/
│   ├── user_service.py
│   ├── admin_user_service.py
│   └── avatar_service.py
│
└── core/
    ├── security.py
    └── storage.py
```

As Plantive grows, these can eventually be grouped into domain-oriented modules, but there is no need to prematurely restructure the entire project.

---

# 5. Database Model

The User model is shared with Module 1.

Conceptually:

```python
class User(SQLModel, table=True):
    id: UUID
    email: str
    hashed_password: str
    full_name: str
    avatar_url: str | None

    role: str
    is_active: bool
    is_verified: bool

    created_at: datetime
    updated_at: datetime
```

The exact model implementation should be established in the Authentication/User database design rather than duplicated between modules.

---

# 6. Database Constraints and Indexes

Application validation is not sufficient.

PostgreSQL should enforce important invariants as well.

## Required Constraints

### Email

```text
UNIQUE(email)
```

Email normalization should occur before persistence.

### Role

The application validates:

```text
gardener
admin
```

The database may additionally use an enum or check constraint depending on the final schema strategy.

### Active State

```text
is_active
```

must always represent the current account state.

---

## Recommended Indexes

The following fields are likely to be queried frequently:

```text
email
role
is_active
is_verified
created_at
```

For admin search, consider the actual PostgreSQL query pattern before adding indexes.

A simple:

```sql
WHERE email ILIKE '%term%'
   OR full_name ILIKE '%term%'
```

does not automatically become fast merely because normal B-tree indexes exist.

For production-scale data, PostgreSQL-specific indexing strategies such as `pg_trgm` can be considered.

Do not add indexes blindly; indexes improve reads but increase write and storage costs.

---

# 7. Schemas

API schemas should remain separate from SQLModel persistence models.

---

## 7.1 `UserProfileResponse`

```python
class UserProfileResponse(BaseModel):
    id: UUID
    email: EmailStr
    full_name: str
    avatar_url: str | None
    role: UserRole
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime
```

The response must never expose:

```text
hashed_password
```

or other authentication secrets.

---

# 8. User Update Schema

## `UserUpdateSchema`

```python
class UserUpdateSchema(BaseModel):
    full_name: str | None = None
```

Validation:

* Trim whitespace.
* Minimum 2 characters.
* Maximum 100 characters.
* Use `exclude_unset=True`.
* `None` should not unintentionally overwrite the existing value unless that behavior is explicitly desired.

The following fields must **not** exist in this schema:

```text
email
role
is_active
is_verified
hashed_password
```

This is an important security boundary.

The client should not be able to send:

```json
{
  "role": "admin"
}
```

to a normal profile endpoint.

---

# 9. Admin User Update Schema

## `AdminUserUpdateSchema`

```python
class AdminUserUpdateSchema(BaseModel):
    role: UserRole | None = None
    is_active: bool | None = None
    is_verified: bool | None = None
```

Allowed roles:

```text
gardener
admin
```

The schema represents administrative controls rather than normal profile editing.

---

# 10. Pagination Schemas

All list endpoints should use a common pagination contract.

## Pagination Metadata

```python
class PaginationMeta(BaseModel):
    page: int
    page_size: int
    total_items: int
    total_pages: int
```

Example:

```json
{
  "page": 1,
  "page_size": 20,
  "total_items": 142,
  "total_pages": 8
}
```

---

# 11. Pagination Dependency

Pagination parameters should be validated centrally.

Conceptually:

```python
class PaginationParams:
    page: int = 1
    page_size: int = 20
```

Validation:

```text
page >= 1
page_size >= 1
page_size <= 100
```

Database pagination:

```text
offset = (page - 1) * page_size
limit = page_size
```

For this project, offset pagination is appropriate initially.

Later, if Plantive contains very large datasets, cursor/keyset pagination can be introduced for specific high-volume endpoints.

---

# 12. Standard Paginated Response

List endpoints should follow:

```json
{
  "success": true,
  "message": "Users retrieved successfully.",
  "data": [],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 142,
    "total_pages": 8
  }
}
```

The pagination metadata belongs at the response-envelope level.

---

# 13. Dependencies

## 13.1 `get_current_user`

Provided by the Authentication module.

```python
async def get_current_user(...) -> User:
    ...
```

Responsibilities:

1. Extract Access JWT.
2. Validate JWT.
3. Validate token type.
4. Extract user ID.
5. Retrieve user.
6. Ensure the account is active.
7. Return the authenticated user.

---

# 14. RBAC Dependency

Create a reusable dependency factory:

```python
def require_role(required_role: UserRole):
    async def role_dependency(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role != required_role:
            raise InsufficientPermissionsError()

        return current_user

    return role_dependency
```

Usage:

```python
current_admin: User = Depends(require_role("admin"))
```

The exact typing implementation can be refined when the `UserRole` enum is introduced.

---

# 15. Why RBAC Belongs in Dependencies

Without a reusable dependency, developers may accidentally write:

```python
if current_user.role != "admin":
    ...
```

inside every controller.

That creates duplicated authorization logic.

Instead:

```text
Router
   ↓
require_role("admin")
   ↓
Controller
```

Every admin endpoint receives the same authorization policy.

This gives us a single place to improve RBAC later.

---

# 16. Repository Layer

The repository handles PostgreSQL/SQLModel persistence.

## `UserRepository`

Recommended responsibilities:

```python
class UserRepository:

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        ...

    async def get_many(
        self,
        *,
        offset: int,
        limit: int,
        search: str | None = None,
        role: UserRole | None = None,
        is_active: bool | None = None,
        is_verified: bool | None = None,
    ) -> tuple[list[User], int]:
        ...

    async def update(
        self,
        user: User,
    ) -> User:
        ...

    async def deactivate(
        self,
        user: User,
    ) -> User:
        ...
```

The repository should not:

* Perform RBAC checks.
* Return HTTP responses.
* Know about FastAPI.
* Generate JWTs.
* Delete Redis sessions.
* Upload avatars.
* Decide whether an admin is allowed to modify a user.

---

# 17. Aggregation Repositories

User history endpoints should normally use repositories belonging to their domain.

For example:

```text
/users/me/gardens
        ↓
GardenRepository

/users/me/orders
        ↓
OrderRepository

/users/me/posts
        ↓
PostRepository
```

Do not put every database query into `UserRepository`.

The fact that a resource belongs to a user does not mean the User repository should own that resource's persistence logic.

This distinction becomes very important as Plantive grows.

---

# 18. Service Layer

## 18.1 `UserService`

Responsible for user-facing operations:

```python
class UserService:

    async def get_profile(...):
        ...

    async def update_profile(...):
        ...

    async def deactivate_account(...):
        ...

    async def upload_avatar(...):
        ...

    async def remove_avatar(...):
        ...

    async def get_user_gardens(...):
        ...

    async def get_user_orders(...):
        ...

    async def get_user_posts(...):
        ...
```

---

# 19. Admin User Service

Administrative operations should be separated from normal self-management.

```python
class AdminUserService:

    async def list_users(...):
        ...

    async def get_user(...):
        ...

    async def update_user(...):
        ...

    async def remove_user(...):
        ...
```

The service still performs business-level safety checks even though RBAC has already happened.

For example:

```text
require_role("admin")
        ↓
AdminUserService
        ↓
self-demotion protection
```

Authorization and business invariants are separate concerns.

---

# 20. Avatar Storage Service

Avatar handling should not live directly in the controller.

Recommended abstraction:

```python
class AvatarStorageService:

    async def upload(
        self,
        *,
        user_id: UUID,
        file: UploadFile,
    ) -> str:
        ...

    async def delete(
        self,
        *,
        user_id: UUID,
        avatar_url: str,
    ) -> None:
        ...
```

Storage implementation can later be:

```text
LocalStorage
S3Storage
CloudStorage
```

without changing the User service.

---

# 21. Avatar Upload Security

Avatar upload is an important security boundary.

The client-provided filename and MIME type must **not** be trusted.

The endpoint receives:

```python
file: UploadFile = File(...)
```

but validation must happen independently.

---

## 21.1 Allowed Formats

Only:

```text
JPEG
PNG
WEBP
```

are accepted.

The actual binary content should be inspected using magic-byte/file-signature validation.

Do not rely exclusively on:

```python
file.content_type
```

because clients can send incorrect MIME types.

---

# 22. Avatar Size Limit

Maximum:

```text
2 MB
```

The implementation should enforce the limit while reading the upload rather than blindly loading arbitrarily large files into memory.

Conceptually:

```text
Incoming upload
      ↓
Read chunks
      ↓
Track bytes
      ↓
> 2 MB?
   ├── Yes → Reject
   └── No → Continue
```

This prevents a malicious client from attempting a very large upload.

---

# 23. Avatar Processing

The original image should be transformed into optimized WebP.

```text
JPEG / PNG / WEBP
       ↓
Validate
       ↓
Decode
       ↓
Resize/compress if required
       ↓
WEBP
       ↓
Storage
```

Processing should happen before the final database URL is persisted.

The storage key should be deterministic or versioned.

Example:

```text
avatars/{user_id}.webp
```

For a future CDN/cache strategy, a versioned filename can be considered:

```text
avatars/{user_id}/{avatar_version}.webp
```

---

# 24. Avatar Upload Consistency

The database and object storage are separate systems.

Therefore, this sequence:

```text
Upload storage
     ↓
Update database
```

can fail halfway.

For example:

```text
Storage upload succeeds
Database update fails
```

Now an orphaned object exists.

Or:

```text
Database update succeeds
Storage deletion fails
```

Now the database points to the new state while old storage remains.

For the initial Plantive implementation, the service should at minimum:

* Handle storage failures.
* Avoid committing invalid avatar URLs.
* Log cleanup failures.
* Keep database state consistent with the known successful storage operation.

Later, an asynchronous cleanup/outbox strategy can be introduced if required.

---

# 25. `GET /api/v1/users/me`

Retrieves the authenticated user's profile.

### Authentication

Bearer Access Token.

Roles:

```text
gardener
admin
```

### Rate Limit

`60 requests/minute`

### Database

`User`

### Flow

```text
Request
  ↓
Access JWT
  ↓
get_current_user
  ↓
UserService.get_profile()
  ↓
UserProfileResponse
  ↓
200 OK
```

### Response

```json
{
  "success": true,
  "message": "User profile retrieved successfully.",
  "data": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "email": "gardener@plantive.com",
    "full_name": "Jane Doe",
    "avatar_url": "https://cdn.plantive.com/avatars/123e4567.webp",
    "role": "gardener",
    "is_active": true,
    "is_verified": true,
    "created_at": "2026-03-15T10:30:00Z",
    "updated_at": "2026-08-01T14:20:00Z"
  }
}
```

---

# 26. `PATCH /api/v1/users/me`

Updates editable profile fields.

### Authentication

Bearer Access Token.

### Rate Limit

`15 requests/minute`

### Request

```json
{
  "full_name": "Jane Smith"
}
```

### Flow

```text
JWT
 ↓
get_current_user
 ↓
UserUpdateSchema
 ↓
UserService.update_profile()
 ↓
Repository.update()
 ↓
Commit
 ↓
200 OK
```

### Update Semantics

Use:

```python
model_dump(exclude_unset=True)
```

so omitted fields are not accidentally overwritten.

The service should update:

```text
updated_at = current UTC time
```

---

# 27. `DELETE /api/v1/users/me`

Self-deactivates the current account.

### Authentication

Bearer Access Token.

### Rate Limit

`3 requests/minute`

### Flow

```text
JWT
 ↓
get_current_user
 ↓
UserService.deactivate_account()
 ↓
is_active = False
 ↓
Revoke refresh sessions
 ↓
Commit
 ↓
200 OK
```

### Important

This is a soft delete.

The User row remains in PostgreSQL.

---

# 28. Refresh Token Revocation

Self-deactivation must invalidate all active sessions.

Conceptually:

```text
auth:refresh:{user_id}:*
```

All matching active refresh-token records must be revoked.

For Redis, do not blindly use expensive production-wide key scanning for every request.

A better design is to maintain a user-level session index/set, for example:

```text
auth:refresh:{user_id}:sessions
```

containing active `jti` values.

Then:

```text
User deactivation
       ↓
Get active jtis
       ↓
Delete individual refresh keys
       ↓
Delete session index
```

This preserves the original Redis design while making mass revocation safer at scale.

---

# 29. `POST /api/v1/users/me/avatar`

Uploads or replaces the user's avatar.

### Authentication

Bearer Access Token.

### Rate Limit

`10 requests/minute`

### Content Type

```text
multipart/form-data
```

### Flow

```text
UploadFile
    ↓
Check upload size
    ↓
Inspect magic bytes
    ↓
Validate image
    ↓
Convert to WebP
    ↓
Upload to storage
    ↓
Update user.avatar_url
    ↓
Commit
    ↓
200 OK
```

### Success

```text
Avatar uploaded successfully.
```

### Invalid Upload

```text
File must be a JPEG, PNG, or WEBP image under 2MB.
```

---

# 30. `DELETE /api/v1/users/me/avatar`

Removes the custom avatar.

### Authentication

Bearer Access Token.

### Rate Limit

`10 requests/minute`

### Flow

```text
Current User
     ↓
avatar_url exists?
 ├── No → 200 "No avatar to remove"
 └── Yes
      ↓
Delete storage object
      ↓
avatar_url = None
      ↓
Commit
      ↓
200 OK
```

Deleting a non-existent avatar should be idempotent.

---

# 31. `GET /api/v1/users/me/gardens`

Returns a paginated summary of gardens owned by the authenticated user.

### Authentication

Bearer Access Token.

### Query Parameters

```text
page=1
page_size=10
```

### Data

```text
Garden
+
Plant count
```

The query should ideally calculate the plant count in PostgreSQL rather than loading every Plant object into Python.

Conceptually:

```text
Garden
  ├── id
  ├── name
  └── plant_count
```

This avoids unnecessary database round trips.

---

# 32. `GET /api/v1/users/me/orders`

Returns the authenticated user's marketplace order history.

### Authentication

Bearer Access Token.

### Query Parameters

```text
status
page
page_size
```

Allowed status values:

```text
pending
completed
cancelled
```

The service must always constrain the query by:

```text
current_user.id
```

The client must never be able to retrieve another user's orders by manipulating query parameters.

---

# 33. `GET /api/v1/users/me/posts`

Returns posts created by the authenticated user.

### Authentication

Bearer Access Token.

### Query Parameters

```text
page
page_size
```

The query must always use:

```text
Post.user_id == current_user.id
```

---

# 34. Admin User Listing

## `GET /api/v1/admin/users`

Lists users with filtering, searching, and pagination.

### Authentication

```python
Depends(require_role("admin"))
```

### Rate Limit

`30 requests/minute`

### Query Parameters

| Parameter     | Type               | Default |
| ------------- | ------------------ | ------- |
| `search`      | `string \| None`   | `None`  |
| `role`        | `UserRole \| None` | `None`  |
| `is_active`   | `bool \| None`     | `None`  |
| `is_verified` | `bool \| None`     | `None`  |
| `page`        | `int`              | `1`     |
| `page_size`   | `int`              | `20`    |

Maximum:

```text
page_size = 100
```

---

# 35. Admin User Query Design

Filtering should be composed in the repository/query layer.

Conceptually:

```text
Base User Query
      │
      ├── search?
      ├── role?
      ├── is_active?
      ├── is_verified?
      │
      ▼
   Count Query
      │
      ▼
   Data Query
      │
      ├── offset
      └── limit
```

Avoid loading all users into Python and filtering there.

Filtering and pagination should happen in PostgreSQL.

---

# 36. Admin User Response

```json
{
  "success": true,
  "message": "Users retrieved successfully.",
  "data": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "gardener@plantive.com",
      "full_name": "Jane Doe",
      "role": "gardener",
      "is_active": true,
      "is_verified": true,
      "created_at": "2026-03-15T10:30:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  }
}
```

---

# 37. `GET /api/v1/admin/users/{id}`

Retrieves a specific user's administrative profile.

### Authentication

Admin only.

### Path Parameter

```text
id: UUID
```

### Flow

```text
JWT
 ↓
get_current_user
 ↓
require_role("admin")
 ↓
AdminUserService.get_user(id)
 ↓
UserRepository.get_by_id(id)
 ↓
200 OK
```

If the target user doesn't exist:

```text
404 Not Found
```

---

# 38. `PATCH /api/v1/admin/users/{id}`

Allows an administrator to modify administrative user controls.

### Authentication

Admin only.

### Request

```json
{
  "role": "admin",
  "is_active": true,
  "is_verified": true
}
```

### Allowed Fields

```text
role
is_active
is_verified
```

### Business Rules

#### Role

Must be:

```text
gardener
admin
```

#### Self-Demotion

An administrator cannot change their own role from:

```text
admin → gardener
```

This rule belongs in the service layer.

#### Deactivation

If:

```text
is_active = False
```

then all active refresh sessions belonging to the target user must be revoked.

---

# 39. `DELETE /api/v1/admin/users/{id}`

Administratively removes/deactivates a user.

### Authentication

Admin only.

### Query Parameter

```text
hard_delete=false
```

### Default Behavior

Soft delete:

```text
user.is_active = False
```

and revoke active refresh sessions.

---

## 39.1 Self-Deletion Guard

An admin cannot delete their own account through this endpoint.

```text
target_user_id == current_admin.id
        ↓
400 Bad Request
```

Message:

```text
Admins cannot delete their own account.
```

This prevents an administrator from accidentally removing their own administrative access through an administrative user-management operation.

---

# 40. Hard Delete Safety

When:

```text
hard_delete=true
```

the service must not simply execute:

```sql
DELETE FROM user WHERE id = ...
```

without reviewing relationships.

Plantive will eventually have relationships such as:

```text
User
 ├── Gardens
 ├── Plants
 ├── Orders
 ├── Order Items
 ├── Posts
 ├── Comments
 ├── Likes
 ├── Reminders
 └── other historical records
```

Therefore, before enabling hard deletion, each foreign key must have an intentional deletion policy:

```text
CASCADE
SET NULL
RESTRICT
```

depending on the business requirement.

Hard deletion should therefore be treated as a separate data-lifecycle operation rather than ordinary user management.

---

# 41. Error Handling

This module should use the application's centralized exception system.

Recommended domain exceptions:

```python
class UserNotFoundError(Exception):
    pass


class InsufficientPermissionsError(Exception):
    pass


class CannotModifyOwnAdminRoleError(Exception):
    pass


class CannotDeleteOwnAccountError(Exception):
    pass


class InvalidAvatarError(Exception):
    pass


class AvatarTooLargeError(Exception):
    pass
```

Exception handlers translate these into the standard response envelope.

---

# 42. HTTP Status Matrix

| Situation                    | Status |
| ---------------------------- | -----: |
| Successful profile retrieval |  `200` |
| Successful profile update    |  `200` |
| Successful deactivation      |  `200` |
| Successful avatar upload     |  `200` |
| Successful avatar deletion   |  `200` |
| Invalid authentication       |  `401` |
| Insufficient permissions     |  `403` |
| Invalid request              |  `400` |
| Target user not found        |  `404` |
| Rate limit exceeded          |  `429` |

---

# 43. Security Requirements

## Authentication

All `/users/me/*` endpoints must require a valid Access Token.

## Authorization

All `/admin/users/*` endpoints must require:

```text
role = admin
```

## IDOR Protection

The following endpoints must never accept a client-provided user ID:

```text
/users/me
/users/me/*
```

The target user must come from:

```text
current_user.id
```

This protects against Insecure Direct Object Reference vulnerabilities.

---

# 44. Sensitive Fields

Never expose these through User API responses:

```text
hashed_password
password reset token
refresh token
JWT
internal session identifiers
```

Administrative endpoints may expose additional operational metadata, but authentication secrets must remain private.

---

# 45. Redis Requirements

This module reuses the Authentication module's refresh-token state.

### Existing Refresh Key

```text
auth:refresh:{user_id}:{jti}
```

### Recommended Session Index

```text
auth:refresh:{user_id}:sessions
```

The session index allows efficient revocation of all sessions when:

```text
user deactivates
admin deactivates user
password is reset
```

---

# 46. Testing Strategy

Testing should cover:

```text
Unit Tests
Integration Tests
API Tests
Security Tests
Database Tests
```

---

# 47. Profile Tests

### `GET /users/me`

Test:

* Valid user.
* Gardener user.
* Admin user.
* Missing token.
* Expired token.
* Deactivated user.
* Correct response fields.
* No password leakage.

### `PATCH /users/me`

Test:

* Valid full name.
* Missing fields.
* `exclude_unset=True`.
* Invalid name length.
* Whitespace trimming.
* Attempt to inject `role`.
* Attempt to inject `is_active`.
* Attempt to inject `is_verified`.
* `updated_at` changes.

---

# 48. Account Deactivation Tests

Test:

* Current user becomes inactive.
* Refresh sessions are revoked.
* Database transaction commits.
* Historical user record remains.
* Repeated deactivation behaves safely.
* Authentication cannot use an inactive account.

---

# 49. Avatar Tests

Test:

### Valid

* JPEG.
* PNG.
* WebP.
* File under 2 MB.
* Existing avatar replacement.

### Invalid

* Unsupported MIME type.
* Fake file extension.
* Invalid magic bytes.
* File larger than 2 MB.
* Corrupt image.

### Storage

* Upload succeeds.
* Database URL updated.
* Storage failure doesn't leave an invalid database state.
* Old avatar cleanup is handled.

### Delete

* Existing avatar.
* No avatar.
* Storage deletion failure.
* Database update.

---

# 50. User Resource Tests

## Gardens

Test:

* Only current user's gardens returned.
* Pagination.
* Correct plant count.
* Empty result.
* Invalid page.
* Maximum page size.

## Orders

Test:

* Only current user's orders returned.
* Status filter.
* Pagination.
* Empty result.

Critical test:

```text
User A must never receive User B's orders.
```

## Posts

Test:

* Only current user's posts returned.
* Pagination.
* Empty result.

---

# 51. Admin RBAC Tests

Every admin endpoint must have tests for:

```text
Admin → allowed
Gardener → 403
Unauthenticated → 401
```

This should be tested for every administrative route, not just one route.

---

# 52. Admin Listing Tests

Test:

* List users.
* Search by email.
* Search by full name.
* Filter by role.
* Filter by active state.
* Filter by verification state.
* Combined filters.
* Pagination.
* Empty result.
* `page_size > 100`.
* Invalid page.
* Correct total count.
* Correct total pages.

---

# 53. Admin Update Tests

Test:

* Promote gardener to admin.
* Keep admin as admin.
* Deactivate user.
* Reactivate user.
* Manually verify user.
* Invalid role.
* Admin self-demotion.
* Refresh-token revocation when deactivated.

Critical invariant:

```text
Admin cannot demote themselves.
```

---

# 54. Admin Delete Tests

Test:

* Soft delete.
* Hard delete.
* Default `hard_delete=False`.
* Self-delete protection.
* Target user not found.
* Refresh-token revocation.
* Database relationships during hard deletion.

Hard-delete tests should use a dedicated test database and explicitly verify foreign-key behavior.

---

# 55. Production Query Rules

For this module, follow these rules:

### Rule 1

Never fetch every record and paginate in Python.

Bad:

```python
users = await get_all_users()
users = users[offset:offset + limit]
```

Good:

```text
PostgreSQL
   ↓
OFFSET
LIMIT
```

### Rule 2

Don't load relationships unnecessarily.

For example, `/users/me/gardens` should not load every Plant object merely to calculate a count.

### Rule 3

Use PostgreSQL for filtering.

```text
WHERE
ORDER BY
LIMIT
OFFSET
COUNT
```

should happen in the database.

### Rule 4

Avoid N+1 queries.

If one endpoint returns 20 gardens and then performs one query per garden:

```text
1 + 20 queries = 21 queries
```

that's an N+1 problem.

Design the SQL query deliberately.

---

# 56. Service Transaction Ownership

A useful rule for Plantive:

> The service owns the business transaction boundary.

For example:

```text
Controller
    ↓
UserService
    ↓
Repository
    ↓
SQLModel Session
    ↓
PostgreSQL
```

The repository should not randomly call `commit()` after every operation if the service needs to coordinate multiple database changes.

This becomes especially important when implementing:

```text
deactivation
admin update
password changes
avatar updates
```

---

# 57. Observability

Important events should be logged:

```text
user.profile.updated
user.account.deactivated
user.avatar.uploaded
user.avatar.removed
admin.user.viewed
admin.user.updated
admin.user.deactivated
admin.user.hard_deleted
```

Logs must not contain:

```text
JWT
password
refresh token
reset token
authentication headers
```

Administrative actions should include enough context for auditing:

```text
admin_user_id
target_user_id
action
timestamp
request_id
```

---

# 58. Audit Consideration

Because administrators can:

* Promote users
* Deactivate users
* Verify users
* Delete users

a production system should eventually maintain an audit trail.

A future model could be:

```text
AdminAuditLog
-------------------------
id
admin_user_id
target_user_id
action
old_value
new_value
created_at
```

This does not need to be implemented immediately if it belongs to a later Administration/Audit module, but the current architecture should leave room for it.

---

# 59. Module-Level Architecture

The complete request flow should look like:

```text
                         HTTP Request
                              │
                              ▼
                         Middleware
                              │
                              ▼
                           Router
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
        get_current_user()         require_role("admin")
                 │                         │
                 └────────────┬────────────┘
                              ▼
                         Controller
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
              UserService       AdminUserService
                    │                   │
          ┌─────────┼─────────┐         │
          │         │         │         │
          ▼         ▼         ▼         ▼
       UserRepo  GardenRepo OrderRepo UserRepo
          │         │         │         │
          └─────────┴─────────┴─────────┘
                              │
                              ▼
                         PostgreSQL

Additional infrastructure:

UserService
    ├── Redis
    └── AvatarStorageService

AdminUserService
    └── Redis
```

---

# 60. Module Responsibilities

| Layer             | Responsibility                                       |
| ----------------- | ---------------------------------------------------- |
| Router            | HTTP routes and FastAPI dependencies                 |
| Controller        | HTTP/application coordination                        |
| Schema            | Request/response validation                          |
| Dependency        | Authentication, RBAC, request-scoped objects         |
| Service           | User/business rules                                  |
| Admin Service     | Administrative business rules                        |
| Repository        | PostgreSQL/SQLModel persistence                      |
| Avatar Service    | File validation, processing, storage                 |
| Redis             | Session/token revocation                             |
| PostgreSQL        | Durable user/domain state                            |
| Exception Handler | Domain exception → HTTP response                     |
| Middleware        | Cross-cutting HTTP concerns                          |
| Tests             | Functional, security, database, integration coverage |

---

# 61. Core Design Invariants

The following rules should remain true regardless of future refactoring.

### Self-management

```text
/users/me/*
        ↓
current_user.id
```

Never:

```text
client_user_id
```

### Admin operations

```text
/admin/users/*
        ↓
authenticated user
        ↓
role == admin
```

### Normal deletion

```text
DELETE
  ↓
is_active = False
  ↓
revoke sessions
```

### Profile update

```text
UserUpdateSchema
        ↓
Only explicitly allowed fields
```

### Avatar

```text
Untrusted upload
        ↓
Size validation
        ↓
Magic-byte validation
        ↓
Image processing
        ↓
Storage
        ↓
Database URL
```

### Pagination

```text
PostgreSQL
   ↓
filter
   ↓
count
   ↓
limit/offset
   ↓
standard envelope + meta
```

### RBAC

```text
Authentication ≠ Authorization
```

A valid JWT proves identity.

The `admin` role determines whether administrative operations are permitted.

---

# 62. Implementation Order

For learning and maintainability, implement Module 2 in this order:

```text
1. User SQLModel model refinement
        ↓
2. Alembic migration
        ↓
3. User schemas
        ↓
4. User repository
        ↓
5. get_current_user dependency
        ↓
6. GET /users/me
        ↓
7. PATCH /users/me
        ↓
8. DELETE /users/me
        ↓
9. Pagination infrastructure
        ↓
10. User gardens/orders/posts
        ↓
11. RBAC dependency
        ↓
12. Admin user listing
        ↓
13. Admin user detail
        ↓
14. Admin user update
        ↓
15. Admin user deletion
        ↓
16. Avatar storage service
        ↓
17. Avatar upload/delete
        ↓
18. Exception handling
        ↓
19. Security tests
        ↓
20. Integration tests
        ↓
21. Performance/query review
        ↓
22. Production review
```

This order intentionally builds the simpler concepts before introducing the more infrastructure-heavy avatar and administrative functionality.

---

# 63. Production Acceptance Checklist

Before considering Module 2 complete:

### Database

* [ ] User constraints reviewed.
* [ ] Required indexes added.
* [ ] Alembic migration reviewed manually.
* [ ] Foreign-key behavior documented.
* [ ] Transactions tested.

### Authentication

* [ ] `get_current_user` implemented.
* [ ] Inactive users rejected.
* [ ] Access JWT validated.
* [ ] User ID derived from JWT for `/me`.

### RBAC

* [ ] `require_role("admin")` implemented.
* [ ] All admin endpoints protected.
* [ ] Gardener receives `403`.
* [ ] Admin self-demotion blocked.
* [ ] Admin self-deletion blocked.

### Profile

* [ ] Profile retrieval implemented.
* [ ] Profile update schema restricts fields.
* [ ] `updated_at` maintained.
* [ ] Sensitive fields excluded.

### Account Lifecycle

* [ ] Self-deactivation implemented.
* [ ] Admin deactivation implemented.
* [ ] Refresh sessions revoked.
* [ ] Hard-delete behavior documented and tested.

### Avatar

* [ ] 2 MB limit enforced.
* [ ] Magic-byte validation.
* [ ] JPEG/PNG/WebP only.
* [ ] WebP processing.
* [ ] Storage abstraction implemented.
* [ ] Storage failures handled.
* [ ] Old avatar cleanup considered.

### Pagination

* [ ] Shared pagination schema.
* [ ] `page >= 1`.
* [ ] `page_size <= 100`.
* [ ] Database-level pagination.
* [ ] Correct total count.
* [ ] Correct total pages.

### Testing

* [ ] Unit tests.
* [ ] API tests.
* [ ] RBAC tests.
* [ ] IDOR tests.
* [ ] Pagination tests.
* [ ] Avatar security tests.
* [ ] Database integration tests.
* [ ] Hard-delete tests.

### Production

* [ ] No secrets in logs.
* [ ] Admin actions auditable.
* [ ] No N+1 queries.
* [ ] Query plans reviewed for important list endpoints.
* [ ] Redis revocation strategy tested.
* [ ] Error responses use the standard envelope.
