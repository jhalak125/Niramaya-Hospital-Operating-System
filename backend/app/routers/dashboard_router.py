from fastapi import APIRouter, Depends

from app.services.dashboard_service import DashboardService

from app.dependencies.role_dependency import require_roles

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/admin")
async def admin_dashboard(
    current_user=Depends(require_roles("admin"))
):

    return await DashboardService.get_admin_dashboard()

@router.get("/doctor")
async def doctor_dashboard(
    current_user=Depends(require_roles("doctor"))
):

    return await DashboardService.get_doctor_dashboard(
        current_user["sub"]
    )

@router.get("/patient")
async def patient_dashboard(
    current_user=Depends(require_roles("patient"))
):

    return await DashboardService.get_patient_dashboard(
        current_user["sub"]
    )