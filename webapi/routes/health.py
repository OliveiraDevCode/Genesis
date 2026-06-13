from fastapi import APIRouter, Request, HTTPException, status
from infrastructure.shared.constants.application_constants import (
    ApplicationConstants
)

router = APIRouter()

@router.get("/health")
async def health(request: Request):

    if not request.app.state.started:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Application not started"
        )

    return {
        "service": ApplicationConstants.SERVICE_NAME,
        "status": "healthy"
    }