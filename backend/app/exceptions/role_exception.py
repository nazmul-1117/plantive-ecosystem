from app.exceptions.base_exception import AppException
from fastapi import status

class RoleNotFound(AppException):
    """
    Raised when a role does not exist
    """

    def __init__(self):
        super().__init__(
            message=f"Role not found.",
            error_code="ROLE_NOT_FOUND",
            status_code=status.HTTP_404_NOT_FOUND
        )

class RoleAlreadyUsed(AppException):
    """
    Raised when a role already Used
    """

    def __init__(self):
        super().__init__(
            message=f"Role already used.",
            error_code="ROLE_ALREADY_USED",
            status_code=status.HTTP_409_CONFLICT
        )