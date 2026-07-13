# auth_exception
from app.exceptions.base_exception import AppException
from fastapi import status

class InvalidLoginCredentials(AppException):
    """
    Raised when the provided email/username or password is invalid
    """

    def __init__(self):
        super().__init__(
            message="Invalid login credentials.",
            error_code="INVALID_LOGIN_CREDENTIALS",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class InvalidAccessToken(AppException):
    """
    JWT cannot be decoded or has an invalid signature.
    """

    def __init__(self):
        super().__init__(
            message="Invalid access token.",
            error_code="INVALID_ACCESS_TOKEN",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class ExpiredAccessToken(AppException):
    """
    JWT has expired.
    """

    def __init__(self):
        super().__init__(
            message="Access token has expired.",
            error_code="EXPIRED_ACCESS_TOKEN",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class InvalidTokenType(AppException):
    """
    Using a refresh token where an access token is expected (or vice versa).
    """

    def __init__(self):
        super().__init__(
            message="Invalid token type.",
            error_code="INVALID_TOKEN_TYPE",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class UserNotAuthenticated(AppException):
    """
    User could not be authenticated.
    """

    def __init__(self):
        super().__init__(
            message="Authentication required.",
            error_code="AUTHENTICATION_REQUIRED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class PermissionDenied(AppException):
    """
    User is authenticate but insufficient permission
    """

    def __init__(self):
        super().__init__(
            message="Insufficient Permission to perform this task.",
            error_code="PERMISSION_DENIED",
            status_code=status.HTTP_403_FORBIDDEN,
        )

class AccountDisabled(AppException):
    """
    User account is disabled
    """

    def __init__(self):
        super().__init__(
            message="Your account has been disabled.",
            error_code="ACCOUNT_DISABLED",
            status_code=status.HTTP_403_FORBIDDEN,
        )

class AccountNotVerified(AppException):
    """
    Email or Account verification required
    """

    def __init__(self):
        super().__init__(
            message="Account verification required.",
            error_code="ACCOUNT_NOT_VERIFIED",
            status_code=status.HTTP_403_FORBIDDEN,
        )

class AccessTokenRequired(AppException):
    """
    Access token required for performing this task
    """

    def __init__(self):
        super().__init__(
            message="Access token required.",
            error_code="ACCESS_TOKEN_REQUIRED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class RefreshTokenRequired(AppException):
    """
    Refresh token required for performing this task
    """

    def __init__(self):
        super().__init__(
            message="Refresh token required.",
            error_code="REFRESH_TOKEN_REQUIRED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class RevokedAccessToken(AppException):
    """
    Access token is revoked
    """

    def __init__(self):
        super().__init__(
            message="Access token revoked.",
            error_code="ACCESS_TOKEN_REVOKED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

