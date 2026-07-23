from fastapi import APIRouter, Depends

from app.dependencies.role_dependency import require_roles
from app.services.analytics_service import (
    get_dashboard_summary,
    get_revenue_analytics,
    get_top_doctors,
    get_appointment_analytics,
    get_lab_test_analytics,
    get_payment_analytics
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)


@router.get("/dashboard")
async def dashboard(
    current_user=Depends(require_roles("admin"))
):
    return await get_dashboard_summary()

@router.get("/revenue")
async def revenue(
    current_user=Depends(require_roles("admin"))
):
    return await get_revenue_analytics()

@router.get("/top-doctors")
async def top_doctors(
    current_user=Depends(require_roles("admin"))
):
    return await get_top_doctors()

@router.get("/appointments")
async def appointments(
    current_user=Depends(require_roles("admin"))
):
    return await get_appointment_analytics()

@router.get("/lab-tests")
async def lab_tests(
    current_user=Depends(require_roles("admin"))
):
    return await get_lab_test_analytics()

@router.get("/payments")
async def payments(
    current_user=Depends(require_roles("admin"))
):
    return await get_payment_analytics()