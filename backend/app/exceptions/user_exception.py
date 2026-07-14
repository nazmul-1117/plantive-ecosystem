from app.exceptions.base_exception import AppException
from fastapi import status

class UserNotFound(AppException):
    """
    User not found
    """

    def __init__(self):
        super().__init__(
            message="User not found.",
            error_code="USER_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )

class EmailAlreadyExists(AppException):
    """
    Email already exists
    """

    def __init__(self):
        super().__init__(
            message="Email already exists.",
            error_code="EMAIL_ALREADY_EXISTS",
            status_code=status.HTTP_409_CONFLICT
        )

class UsernameAlreadyExists(AppException):
    """
    Username already exists
    """

    def __init__(self):
        super().__init__(
            message="Username already exists.",
            error_code="USERNAME_ALREADY_EXISTS",
            status_code=status.HTTP_409_CONFLICT
        )


class UserInactive(AppException):
    """
    User account is inactive
    """

    def __init__(self):
        super().__init__(
            message="User account is inactive.",
            error_code="USER_INACTIVE",
            status_code=status.HTTP_403_FORBIDDEN,
        )


