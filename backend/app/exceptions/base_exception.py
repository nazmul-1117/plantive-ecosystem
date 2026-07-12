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
            status_code: int = status.HTTP_400_BAD_REQUEST
    ):
        self.message = message
        error_code = error_code
        status_code = status_code

        super().__init__(message)