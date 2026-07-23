from fastapi import APIRouter, Depends

from app.services.audit_log_service import get_all_logs

from app.dependencies.auth_dependency import require_admin


router = APIRouter(

    prefix="/audit-logs",

    tags=["Audit Logs"]

)


@router.get("/")

async def all_logs(

    current_user=Depends(require_admin)

):

    logs = await get_all_logs()

    return {

        "logs": logs

    }