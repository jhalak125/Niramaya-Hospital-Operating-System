from fastapi import APIRouter, Depends, BackgroundTasks

from app.schemas.appointment_schema import (
    AppointmentCreate,
    AppointmentUpdate
)
from app.schemas.appointment_update_schema import AppointmentStatusUpdate

from app.services.appointment_service import (
    create_appointment,
    get_patient_appointments,
    get_doctor_appointments,
    update_appointment_status,
    get_appointment,
    update_appointment,
    delete_appointment,
    get_all_appointments
)

from app.dependencies.auth_dependency import (
    require_patient,
    require_doctor,
    require_admin,
    require_admin_or_doctor
)
from app.dependencies.role_dependency import require_roles

router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


@router.post("")
@router.post("/")
async def create(
    data: AppointmentCreate,
    background_tasks: BackgroundTasks,
    current_user=Depends(require_patient)
):
    return await create_appointment(
        data,
        background_tasks
    )


@router.get("")
@router.get("/")
async def all_appointments(
    current_user=Depends(require_roles("admin"))
):
    return await get_all_appointments()


@router.get("/my")
async def my_appointments(
    current_user=Depends(require_patient)
):
    appointments = await get_patient_appointments(
        current_user["sub"]
    )
    return {
        "appointments": appointments
    }


@router.get("/doctor")
async def doctor_appointments(
    current_user=Depends(require_doctor)
):
    appointments = await get_doctor_appointments(
        current_user["sub"]
    )
    return {
        "appointments": appointments
    }


@router.get("/{appointment_id}")
async def fetch_appointment(
    appointment_id: str,
    current_user=Depends(require_admin_or_doctor)
):
    return await get_appointment(
        appointment_id
    )


@router.put("/{appointment_id}")
async def edit_appointment(
    appointment_id: str,
    data: AppointmentUpdate,
    current_user=Depends(require_patient)
):
    return await update_appointment(
        appointment_id,
        data
    )


@router.patch("/{appointment_id}/status")
async def update_status(
    appointment_id: str,
    data: AppointmentStatusUpdate,
    current_user=Depends(require_doctor)
):
    return await update_appointment_status(
        appointment_id,
        data.status
    )


@router.delete("/{appointment_id}")
async def remove_appointment(
    appointment_id: str,
    current_user=Depends(require_admin)
):
    return await delete_appointment(
        appointment_id
    )