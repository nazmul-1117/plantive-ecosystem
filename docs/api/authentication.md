# Plantive — Authentication Module

## FastAPI Engineering Specification

> **Module:** Authentication\
> **API Version:** `v1`\
> **Base Path:** `/api/v1/auth`\
> **Status:** Production Specification

---

# 1. Module Overview

The Authentication module is responsible for:

* User registration
* Email verification
* Login
* Access-token issuance
* Refresh-token rotation
* Logout
* Password recovery
* Password reset
* Password changes
* Authentication and authorization dependencies
* Session/token revocation

The implementation should follow a layered architecture:

```text
HTTP Request
    ↓
FastAPI Router
    ↓
Dependencies
    ↓
Service Layer
    ↓
Repository Layer
    ↓
Database / Redis / External Services
```

The router should remain thin. Business rules should live in services, while persistence operations should remain in repositories.

---

# 2. Production Response Envelope

Every API response must use a predictable top-level envelope.

## 2.1 Success Envelope

```json
{
  "success": true,
  "message": "Authentication successful.",
  "data": {}
}
```

### Fields

| Field     | Type             | Required | Description               |
| --------- | ---------------- | -------: | ------------------------- |
| `success` | `boolean`        |      Yes | Indicates request success |
| `message` | `string`         |      Yes | Human-readable result     |
| `data`    | `object \| null` |      Yes | Response payload          |

---

## 2.2 Error Envelope

```json
{
  "success": false,
  "message": "Validation failed on incoming request payload.",
  "errors": [
    {
      "field": "password",
      "issue": "Password must be at least 8 characters and contain at least one special character."
    }
  ]
}
```

### Fields

| Field     | Type      | Required | Description                    |
| --------- | --------- | -------: | ------------------------------ |
| `success` | `boolean` |      Yes | Always `false`                 |
| `message` | `string`  |      Yes | General error message          |
| `errors`  | `array`   |       No | Field-level or detailed errors |

---

# 3. Recommended Project Structure

The Authentication module should be isolated from unrelated application domains.

```text
app/
├── main.py
│
├── core/
│   ├── config.py
│   ├── security.py
│   ├── exceptions.py
│   └── responses.py
│
├── db/
│   ├── session.py
│   └── base.py
│
├── modules/
│   └── auth/
│       ├── router.py
│       ├── schemas.py
│       ├── dependencies.py
│       ├── services.py
│       ├── repositories.py
│       ├── security.py
│       ├── constants.py
│       └── tests/
│           ├── test_register.py
│           ├── test_login.py
│           ├── test_refresh.py
│           ├── test_logout.py
│           ├── test_email_verification.py
│           ├── test_forgot_password.py
│           ├── test_reset_password.py
│           └── test_change_password.py
│
├── models/
│   └── user.py
│
├── services/
│   └── email.py
│
└── redis/
    └── client.py
```

The exact directory names may vary, but the architectural responsibilities should remain separated.

---

# 4. API Route Map

| Method | Route              | Auth                 | Service                    |
| ------ | ------------------ | -------------------- | -------------------------- |
| `POST` | `/register`        | Public               | `register_user()`          |
| `POST` | `/login`           | Public               | `authenticate_user()`      |
| `POST` | `/refresh-token`   | Refresh Token        | `refresh_tokens()`         |
| `POST` | `/logout`          | Access/Refresh Token | `logout_user()`            |
| `GET`  | `/verify-email`    | Public               | `verify_email()`           |
| `POST` | `/forgot-password` | Public               | `request_password_reset()` |
| `POST` | `/reset-password`  | Public               | `reset_password()`         |
| `POST` | `/change-password` | Access Token         | `change_password()`        |

---

# 5. Schemas

Pydantic schemas define the API contract and perform request/response validation.

## 5.1 `UserRegisterSchema`

```python
class UserRegisterSchema(BaseModel):
    email: EmailStr
    password: str
    full_name: str
```

### Validation

* Normalize email to lowercase.
* Password: 8–128 characters.
* Password requires:

  * uppercase
  * lowercase
  * number
  * special character
* `full_name`: trim whitespace.
* `full_name`: 2–100 characters.

---

## 5.2 `UserLoginSchema`

```python
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str
```

Email should be normalized to lowercase before authentication.

---

## 5.3 `ForgotPasswordSchema`

```python
class ForgotPasswordSchema(BaseModel):
    email: EmailStr
```

---

## 5.4 `ResetPasswordSchema`

```python
class ResetPasswordSchema(BaseModel):
    token: str
    new_password: str
```

`new_password` must use the same password-complexity policy as registration.

---

## 5.5 `ChangePasswordSchema`

```python
class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str
```

The service must additionally verify:

```text
new_password != current_password
```

---

## 5.6 `UserReadSchema`

The public user representation should contain only fields intended for API consumers.

```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "gardener@plantive.com",
  "full_name": "Jane Doe",
  "is_active": true,
  "is_verified": false
}
```

Never expose:

* `hashed_password`
* password reset tokens
* refresh-token identifiers
* internal security metadata

---

## 5.7 `TokenResponseSchema`

```json
{
  "success": true,
  "message": "Authentication successful.",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1Ni...",
    "token_type": "bearer",
    "expires_in": 900,
    "user": {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "email": "gardener@plantive.com",
      "full_name": "Jane Doe",
      "role": "gardener"
    }
  }
}
```

---

# 6. Dependencies

FastAPI dependencies provide reusable request-scoped infrastructure and authentication logic.

## 6.1 Database Session

```python
async def get_db() -> AsyncSession:
    ...
```

Responsibilities:

* Provide an `AsyncSession`.
* Ensure proper transaction lifecycle.
* Roll back failed transactions where appropriate.
* Close the session after the request.

---

## 6.2 Redis Client

```python
async def get_redis():
    ...
```

Used for:

* Refresh-token tracking
* Refresh-token revocation
* Password-reset token tracking
* Optional access-token blacklisting
* Rate-limit state if implemented through Redis

---

## 6.3 Current User Dependency

```python
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    ...
```

Responsibilities:

1. Extract Access JWT.
2. Decode and validate token.
3. Verify `type == "access"`.
4. Extract `sub`.
5. Load the user.
6. Verify the account is active.
7. Return the authenticated user.

Routes requiring an active session should depend on `get_current_user`.

---

## 6.4 Refresh Token Dependency

Refresh-token extraction should support:

```text
HttpOnly Cookie: plantive_refresh
```

and, where required:

```text
Authorization: Bearer <refresh_token>
```

The dependency/service must verify that the token is actually a Refresh Token.

---

# 7. Security Layer

Authentication-specific cryptographic operations should be isolated from routers and business services.

## 7.1 Password Hashing

Use:

```text
pwdlib
    ↓
Argon2id
```

Passwords must never be stored in plaintext.

The database stores only:

```text
user.hashed_password
```

---

## 7.2 JWT Types

The Authentication module uses explicit JWT token types.

### Access Token

```json
{
  "sub": "<user_id>",
  "role": "gardener",
  "type": "access",
  "exp": "<15 minutes>"
}
```

### Refresh Token

```json
{
  "sub": "<user_id>",
  "jti": "<uuid>",
  "type": "refresh",
  "exp": "<7 days>"
}
```

### Email Verification Token

```text
type = "email_verify"
TTL = 24 hours
```

### Password Reset Token

```text
type = "password_reset"
TTL = 15 minutes
```

Token type must always be validated before the token is accepted for its intended operation.

---

# 8. Redis Key Specification

Redis is part of the Authentication module's security state.

## 8.1 Refresh Token

```text
auth:refresh:{user_id}:{jti}
```

### TTL

`7 days`

### Purpose

Tracks active refresh tokens and supports:

* Revocation
* Rotation
* Token reuse detection
* Logout

---

## 8.2 Password Reset Token

```text
auth:reset:{user_id}
```

### TTL

`15 minutes`

### Purpose

Ensures that a password-reset token:

* Expires
* Can only be used once
* Can be explicitly invalidated

The stored value should represent the token hash rather than the raw token.

---

## 8.3 Optional Access Token Blacklist

```text
auth:blacklist:{user_id}:{jti}
```

### TTL

Remaining Access Token lifespan.

### Purpose

Optional immediate invalidation of an active Access Token.

---

# 9. Repository Layer

Repositories should contain persistence operations and remain independent of HTTP concerns.

## 9.1 `UserRepository`

Recommended interface:

```python
class UserRepository:

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        ...

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        ...

    async def create(
        self,
        user: User,
    ) -> User:
        ...

    async def update(
        self,
        user: User,
    ) -> User:
        ...
```

The repository should not:

* Return HTTP responses.
* Raise `HTTPException` for business conditions.
* Know about FastAPI routes.
* Generate JWTs.
* Send emails.

---

# 10. Service Layer

Services contain the business logic for the Authentication module.

## 10.1 `AuthService`

Recommended operations:

```python
class AuthService:

    async def register_user(...):
        ...

    async def authenticate_user(...):
        ...

    async def refresh_tokens(...):
        ...

    async def logout_user(...):
        ...

    async def verify_email(...):
        ...

    async def request_password_reset(...):
        ...

    async def reset_password(...):
        ...

    async def change_password(...):
        ...
```

The service coordinates:

```text
Repository
Redis
Security
Email Service
Transaction
```

---

# 11. Email Service

Email delivery should not be implemented directly inside route functions.

Recommended abstraction:

```python
class EmailService:

    async def send_verification_email(
        self,
        email: str,
        token: str,
    ) -> None:
        ...

    async def send_password_reset_email(
        self,
        email: str,
        token: str,
    ) -> None:
        ...
```

Implementation:

```text
EmailService
    ↓
aiosmtplib
    ↓
Jinja2 HTML Template
    ↓
SMTP Provider
```

Email sending should be asynchronous/background work where appropriate.

---

# 12. Endpoint Implementation Specifications

## 12.1 Register

### `POST /api/v1/auth/register`

**Authentication:** Public

**Rate Limit:** `5 requests/minute/IP`

### Flow

```text
Request
  ↓
UserRegisterSchema
  ↓
Normalize email
  ↓
UserRepository.get_by_email()
  ↓
Already exists?
  ├── Yes → 409
  └── No
       ↓
Hash password
       ↓
Create User
       ↓
Generate email verification JWT
       ↓
Commit User
       ↓
Dispatch verification email
       ↓
201 Created
```

User defaults:

```text
is_active = True
is_verified = False
role = "gardener"
```

---

## 12.2 Login

### `POST /api/v1/auth/login`

**Authentication:** Public

**Rate Limit:** `10 requests/minute/IP`

### Flow

```text
Credentials
    ↓
Normalize email
    ↓
Fetch User
    ↓
Verify password
    ↓
Check is_active
    ↓
Generate Access JWT
    ↓
Generate Refresh JWT
    ↓
Store Refresh jti in Redis
    ↓
Set HttpOnly Refresh Cookie
    ↓
Return TokenResponseSchema
```

Access Token:

```text
TTL = 15 minutes
```

Refresh Token:

```text
TTL = 7 days
```

---

## 12.3 Refresh Token

### `POST /api/v1/auth/refresh-token`

**Authentication:** Valid Refresh Token

**Rate Limit:** `30 requests/minute`

### Flow

```text
Extract Refresh Token
       ↓
Decode JWT
       ↓
Verify type=refresh
       ↓
Extract user_id + jti
       ↓
Check Redis
       ↓
Valid?
 ├── No → 401
 └── Yes
       ↓
Delete old jti
       ↓
Generate new Access Token
       ↓
Generate new Refresh Token
       ↓
Store new jti
       ↓
Update Cookie
       ↓
Return token pair
```

This implements **Refresh Token Rotation**.

---

## 12.4 Logout

### `POST /api/v1/auth/logout`

**Authentication:** Access Token or Refresh Token

**Rate Limit:** `20 requests/minute`

### Flow

```text
Extract token context
      ↓
Extract user_id + jti
      ↓
Delete auth:refresh:{user_id}:{jti}
      ↓
Optionally blacklist Access Token
      ↓
Clear plantive_refresh cookie
      ↓
200 OK
```

---

## 12.5 Verify Email

### `GET /api/v1/auth/verify-email`

**Authentication:** Public

**Rate Limit:** `10 requests/minute`

### Query Parameter

```text
token=<verification_jwt>
```

### Flow

```text
Token
  ↓
Decode JWT
  ↓
Verify type=email_verify
  ↓
Extract user_id
  ↓
Load User
  ↓
Already verified?
 ├── Yes → 200 "Email already verified."
 └── No
      ↓
Set is_verified=True
      ↓
Commit
      ↓
200 OK
```

---

## 12.6 Forgot Password

### `POST /api/v1/auth/forgot-password`

**Authentication:** Public

**Rate Limit:** `3 requests/minute/IP`

### Critical Security Requirement

The endpoint must not reveal whether an email address is registered.

Both cases should produce the same public response:

```text
If an account with that email exists, a password reset link has been sent.
```

### Flow

```text
Email
  ↓
Find User
  ↓
Not found?
 └── Return generic 200
  ↓
Generate reset JWT
  ↓
Hash token
  ↓
Store auth:reset:{user_id}
  ↓
Send email
  ↓
200 OK
```

---

## 12.7 Reset Password

### `POST /api/v1/auth/reset-password`

**Authentication:** Public

**Rate Limit:** `5 requests/minute`

### Flow

```text
Reset Token + New Password
        ↓
Decode JWT
        ↓
Verify type=password_reset
        ↓
Check Redis auth:reset:{user_id}
        ↓
Valid?
 ├── No → 400
 └── Yes
       ↓
Validate password
       ↓
Hash password
       ↓
Update User
       ↓
Delete reset Redis key
       ↓
Revoke all refresh tokens
       ↓
200 OK
```

Resetting a password must invalidate existing refresh sessions so that the user is forced to authenticate again across devices.

---

## 12.8 Change Password

### `POST /api/v1/auth/change-password`

**Authentication:** Bearer Access Token

**Rate Limit:** `5 requests/minute`

### Flow

```text
Access Token
    ↓
get_current_user
    ↓
Current Password
    ↓
Verify password
    ↓
Validate new password
    ↓
Ensure new != current
    ↓
Hash new password
    ↓
Update User
    ↓
Commit
    ↓
200 OK
```

---

# 13. Error Handling

HTTP-specific error handling should be centralized.

## 13.1 Authentication Errors

### `401 Unauthorized`

Use when:

* Access token is missing.
* Access token is invalid.
* Access token is expired.
* Refresh token is invalid.
* Refresh token has been revoked.
* Credentials are invalid.

Example:

```json
{
  "success": false,
  "message": "Invalid or expired refresh token.",
  "errors": []
}
```

---

## 13.2 Authorization / Account State

### `403 Forbidden`

Use when authentication succeeds but the account cannot perform the operation.

Example:

```text
Your account has been deactivated. Please contact support.
```

---

## 13.3 Validation Errors

### `400 Bad Request`

Use for application-level validation failures such as:

* Invalid password reset token.
* Incorrect current password.
* Invalid verification token.

Pydantic request-validation errors should also be converted into the standard application response envelope.

---

## 13.4 Conflict

### `409 Conflict`

Used when attempting to register an already-existing email address.

```text
An account with this email address already exists.
```

---

## 13.5 Rate Limiting

### `429 Too Many Requests`

Used when an authentication endpoint exceeds its configured rate limit.

Example:

```text
Too many registration attempts. Please try again later.
```

---

## 13.6 Internal Errors

### `500 Internal Server Error`

Unexpected infrastructure failures must not expose:

* Database details
* Stack traces
* JWT secrets
* Redis errors
* SMTP credentials
* Internal implementation details

The client should receive a safe generic response.

Detailed errors should be logged internally.

---

# 14. Rate-Limit Policy

| Endpoint           |       Limit |
| ------------------ | ----------: |
| `/register`        |  `5/min/IP` |
| `/login`           | `10/min/IP` |
| `/refresh-token`   |    `30/min` |
| `/logout`          |    `20/min` |
| `/verify-email`    |    `10/min` |
| `/forgot-password` |  `3/min/IP` |
| `/reset-password`  |     `5/min` |
| `/change-password` |     `5/min` |

Rate limiting should preferably be backed by Redis in a distributed deployment.

---

# 15. Transaction Boundaries

Database operations that modify user state should use explicit transaction boundaries.

### Registration

```text
Create User
    ↓
Commit
    ↓
Dispatch email
```

### Email Verification

```text
Set is_verified=True
    ↓
Commit
```

### Password Reset

```text
Update password
    ↓
Commit
    ↓
Invalidate reset token
    ↓
Revoke sessions
```

### Password Change

```text
Update password
    ↓
Commit
```

The service layer should control business transaction boundaries rather than individual repository methods committing independently.

---

# 16. Security Requirements

The following requirements are mandatory.

## Password Security

* Use Argon2id.
* Never store plaintext passwords.
* Never log passwords.
* Never include passwords in API responses.
* Validate password complexity consistently.

## JWT Security

* Validate token expiration.
* Validate token type.
* Validate token subject.
* Use a secure signing secret/key.
* Keep Access Tokens short-lived.
* Keep Refresh Tokens revocable.
* Use unique `jti` values for Refresh Tokens.

## Cookie Security

Refresh Token cookies must use:

```text
HttpOnly
Secure
SameSite=Lax
```

Cookie name:

```text
plantive_refresh
```

## Enumeration Protection

Password-reset requests must return the same public response regardless of whether the account exists.

## Timing Attack Protection

Login should perform password verification in a way that does not reveal whether an email exists through measurable timing differences.

A dummy password-hash verification may be used when the user does not exist.

## Session Invalidation

Password reset must revoke active Refresh Tokens.

---

# 17. Testing Specification

Authentication is security-critical and requires unit, integration, and API-level tests.

## 17.1 Registration Tests

### Happy Path

* Valid registration returns `201`.
* User is persisted.
* Password is hashed.
* `is_active=True`.
* `is_verified=False`.
* `role="gardener"`.
* Verification token is generated.
* Verification email is dispatched.

### Validation

Test:

* Invalid email.
* Duplicate email.
* Password below 8 characters.
* Password above 128 characters.
* Missing uppercase.
* Missing lowercase.
* Missing number.
* Missing special character.
* `full_name` below 2 characters.
* `full_name` above 100 characters.

### Security

* Plaintext password never stored.
* Password never returned.
* Duplicate registration returns `409`.

---

# 18. Login Tests

### Happy Path

* Valid credentials return `200`.
* Access Token is returned.
* Refresh Token is generated.
* Refresh `jti` is stored in Redis.
* Refresh cookie is set.

### Failure Cases

* Unknown email → `401`.
* Incorrect password → `401`.
* Deactivated account → `403`.
* Expired credentials/token scenarios behave correctly.

### Security

* Invalid credentials should not reveal whether the email exists.
* Password verification should use the configured password-hashing library.
* Sensitive credentials must not appear in logs.

---

# 19. Refresh Token Tests

Test:

* Valid refresh token.
* Expired refresh token.
* Invalid signature.
* Wrong token type.
* Missing Redis `jti`.
* Revoked refresh token.
* Token reuse.
* Successful token rotation.
* Old `jti` is deleted.
* New `jti` is stored.
* New cookie is set.

Critical invariant:

```text
Old Refresh Token
       ↓
Must NOT remain valid
```

---

# 20. Logout Tests

Test:

* Valid logout.
* Redis refresh key deletion.
* Cookie clearing.
* Optional Access Token blacklist.
* Invalid token behavior.

Critical invariant:

```text
After logout:
Refresh Token → revoked
```

---

# 21. Email Verification Tests

Test:

* Valid verification token.
* Expired token.
* Invalid token.
* Wrong token type.
* Unknown user.
* Already verified user.
* Database commit.
* `is_verified` changes from `False → True`.

---

# 22. Password Reset Tests

## Forgot Password

Test:

* Existing email.
* Unknown email.
* Generic response for both cases.
* Reset JWT generation.
* Redis token hash storage.
* Email dispatch.
* Rate limiting.

Critical invariant:

```text
Unknown email
    ↓
Must NOT reveal account existence
```

## Reset Password

Test:

* Valid token.
* Expired token.
* Invalid token.
* Wrong token type.
* Missing Redis token.
* Mismatched Redis token.
* Password validation.
* Password hashing.
* Redis token deletion.
* Refresh-session revocation.

---

# 23. Change Password Tests

Test:

* Valid current password.
* Incorrect current password.
* Invalid new password.
* New password equal to current password.
* Successful password update.
* Password is hashed.
* Database transaction commits.
* Existing password remains unusable after successful change according to session policy.

---

# 24. Integration Test Matrix

| Scenario                        | Expected |
| ------------------------------- | -------- |
| Register new user               | `201`    |
| Register duplicate email        | `409`    |
| Login valid credentials         | `200`    |
| Login invalid credentials       | `401`    |
| Login inactive account          | `403`    |
| Refresh valid token             | `200`    |
| Refresh revoked token           | `401`    |
| Reuse rotated token             | `401`    |
| Logout                          | `200`    |
| Verify email                    | `200`    |
| Verify expired email token      | `400`    |
| Forgot password existing email  | `200`    |
| Forgot password unknown email   | `200`    |
| Reset valid password            | `200`    |
| Reset invalid token             | `400`    |
| Change valid password           | `200`    |
| Change invalid current password | `400`    |
| Missing Access Token            | `401`    |
| Rate limit exceeded             | `429`    |

---

# 25. Dependency Override Strategy for Tests

FastAPI dependency overrides should be used to isolate external infrastructure.

Example:

```python
app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_redis] = override_get_redis
```

Tests should be able to replace:

* Database session
* Redis client
* Email service
* Authentication dependencies
* External SMTP provider

External email delivery should never be required for ordinary automated tests.

---

# 26. Observability & Logging

Authentication events should be logged without exposing secrets.

Recommended events:

```text
user.registration
user.login.success
user.login.failure
user.email_verified
user.token.refresh
user.token.revoked
user.logout
user.password_reset.requested
user.password_reset.completed
user.password_changed
```

Do **not** log:

* Passwords
* Raw JWTs
* Reset tokens
* Verification tokens
* Refresh tokens
* Cookie values
* Authentication headers

Logs should contain safe identifiers such as:

```text
user_id
request_id
event
timestamp
IP metadata where appropriate
```

---

# 27. Authentication Invariants

The following invariants must always hold.

### Password

```text
Plain Password
    ↓
Argon2id
    ↓
hashed_password
```

Never:

```text
Plain Password → Database
```

### Access Token

```text
Short-lived
+
Signed
+
type=access
```

### Refresh Token

```text
Signed
+
Unique jti
+
Redis tracked
+
Rotated
+
Revocable
```

### Password Reset

```text
Short-lived JWT
+
Redis single-use state
+
Password update
+
Refresh-session revocation
```

### Password Enumeration

```text
Existing Email ─┐
                ├── Same Public Response
Unknown Email ──┘
```

---

# 28. Final Architecture

The resulting Authentication module should follow this dependency direction:

```text
                    ┌──────────────────┐
                    │   FastAPI Router │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Dependencies   │
                    │                  │
                    │ get_db           │
                    │ get_redis        │
                    │ get_current_user │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Auth Service   │
                    │                  │
                    │ register         │
                    │ login            │
                    │ refresh          │
                    │ logout           │
                    │ verify email     │
                    │ reset password   │
                    │ change password  │
                    └─────┬─────┬────┘
                          │     │
              ┌───────────┘     └────────────┐
              ▼                              ▼
     ┌─────────────────┐            ┌─────────────────┐
     │ User Repository │            │ Security Layer  │
     └────────┬────────┘            └────────┬────────┘
              │                              │
              ▼                              ▼
        ┌───────────┐                ┌────────────────┐
        │ PostgreSQL│                │ JWT / Argon2id │
        └───────────┘                └────────────────┘
                          │
                          ▼
                    ┌────────────┐
                    │   Redis    │
                    │            │
                    │ Refresh    │
                    │ Reset      │
                    │ Blacklist  │
                    │ Rate Limit │
                    └────────────┘

                          │
                          ▼
                    ┌────────────┐
                    │Email Service│
                    │            │
                    │ aiosmtplib │
                    │  Jinja2    │
                    └────────────┘
```

## Layer Responsibilities

| Layer             | Responsibility                                   |
| ----------------- | ------------------------------------------------ |
| **Router**        | HTTP contract, request/response handling         |
| **Schema**        | Input/output validation                          |
| **Dependencies**  | Request-scoped infrastructure and authentication |
| **Service**       | Business rules and orchestration                 |
| **Repository**    | Database persistence                             |
| **Security**      | Password hashing and JWT operations              |
| **Redis**         | Token/session security state and rate limiting   |
| **Email Service** | Verification/reset email delivery                |
| **Model**         | Database representation                          |
| **Tests**         | Unit, integration, security, and API behavior    |

The key architectural rule is:

> **Routes should describe HTTP behavior; services should contain business behavior; repositories should contain persistence behavior.**
