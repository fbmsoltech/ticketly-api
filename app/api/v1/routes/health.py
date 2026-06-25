from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Verifica o estado da API")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
