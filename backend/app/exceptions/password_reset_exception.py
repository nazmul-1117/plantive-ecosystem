
from app.exceptions.base_exception import AppException
from fastapi import status

class InvalidPasswordResetTokenError(AppException):
    """
    Raised when the provided password reset token is invalid
    """

    def __init__(self):
        super().__init__(
            message="Invalid password reset token.",
            error_code="INVALID_PASSWORD_RESET_TOKEN",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class PasswordResetTokenExpiredError(AppException):
    """
    Raised when the provided password reset token is expired.
    """

    def __init__(self):
        super().__init__(
            message="Expired password reset token.",
            error_code="EXPIRED_PASSWORD_RESET_TOKEN",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class PasswordResetTokenAlreadyUsedError(AppException):
    """
    Raised when the provided password reset token already used.
    """

    def __init__(self):
        super().__init__(
            message="Password reset token already used.",
            error_code="PASSWORD_RESET_TOKEN_ALREADY_USED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

class PasswordResetTokenRevokedError(AppException):
    """
    Raised when the provided password reset token revoked.
    """

    def __init__(self):
        super().__init__(
            message="Password reset token already Revoked.",
            error_code="PASSWORD_RESET_TOKEN_ALREADY_REVOKED",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )