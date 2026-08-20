
# app/depedencies/query_validation_dependency.py

from collections.abc import Callable
from typing import TypeVar

from fastapi import HTTPException, Request, status
from pydantic import BaseModel

SchemaT = TypeVar("SchemaT", bound=BaseModel)

def strict_query_params(
        schema: type[SchemaT],
) -> Callable:

    async def dependency(
            request: Request,
    ) -> None:

        allowed_params = set(schema.model_fields)
        received_params = set(request.query_params.keys())
        unknown_params = received_params - allowed_params

        if unknown_params:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail=[
                    {
                        "loc": ["query", param],
                        "msg": "Extra inputs are not permitted",
                        "type": "extra_forbidden",
                    }
                    for param in sorted(unknown_params)
                ],
            )

    return dependency