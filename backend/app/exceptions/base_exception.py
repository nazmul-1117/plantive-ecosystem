from fastapi import status

class AppException(Exception):
    """
    Base Appliicaon Exception.
    """

    def __init__(
            self,
            *,
            message: str,
            error_code: str,
            status_code: int = status.HTTP_400_BAD_REQUEST,
            details: dict | None = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}

        super().__init__(message)