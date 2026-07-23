from fastapi import APIRouter, Depends

from app.schemas.doctor_schema import DoctorCreate
from app.schemas.doctor_schema import DoctorUpdate

from app.services.doctor_service import (
    create_doctor,
    get_doctor,
    update_doctor,
    delete_doctor
)
from app.dependencies.role_dependency import require_roles
from app.repositories.doctor_repository import DoctorRepository
from app.utils.serializer import doctors_serializer
from typing import Optional
from app.services.doctor_service import search_doctors

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


@router.post("/")
async def add_doctor(
    doctor: DoctorCreate,
    current_user=Depends(require_roles("admin"))
):
    return await create_doctor(doctor)


from app.services.doctor_service import get_all_doctors


@router.get("/")
async def get_all():
    return await get_all_doctors()

@router.get("/search")
async def search(
    department: Optional[str] = None,
    specialization: Optional[str] = None,
    status: Optional[str] = None,
    min_experience: Optional[int] = None,
    page: int = 1,
    limit: int = 10,
    sort_by: Optional[str] = None,
    order: str = "asc"
):

    doctors = await search_doctors(
        department,
        specialization,
        status,
        min_experience,
        page,
        limit,
        sort_by,
        order
    )

    return doctors_serializer(doctors)

@router.put("/{doctor_id}")
async def edit_doctor(
    doctor_id: str,
    doctor: DoctorUpdate,
    current_user=Depends(
        require_roles("admin")
    )
):
    return await update_doctor(
        doctor_id,
        doctor
    )

@router.delete("/{doctor_id}")
async def remove_doctor(
    doctor_id: str,
    current_user=Depends(
        require_roles("admin")
    )
):
    return await delete_doctor(
        doctor_id
    )

from app.services.doctor_service import get_doctor


@router.get("/{doctor_id}")
async def fetch_doctor(
    doctor_id: str
):

    return await get_doctor(doctor_id)