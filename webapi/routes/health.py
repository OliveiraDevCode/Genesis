from fastapi import APIRouter, Depends

from application.use_cases.health import HealthCheckUseCase
from webapi.dependencies import get_health_use_case, get_settings
from webapi.settings import Settings

router = APIRouter()


@router.get("/health")
async def health(
    use_case: HealthCheckUseCase = Depends(get_health_use_case),
    settings: Settings = Depends(get_settings),
):
    result = use_case.execute()
    result["service"] = settings.service_name
    result["environment"] = settings.environment
    return result
