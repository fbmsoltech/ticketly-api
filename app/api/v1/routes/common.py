from typing import NoReturn

from fastapi import HTTPException, status


def raise_not_found(entity_name: str) -> NoReturn:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity_name} not found",
    )
