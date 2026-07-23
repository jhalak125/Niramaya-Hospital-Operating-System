from fastapi import APIRouter, Depends

from app.schemas.patient_schema import PatientCreate
from app.services.patient_service import create_patient
from app.services.patient_service import get_patient
from app.dependencies.role_dependency import require_roles
from app.services.patient_service import get_all_patients

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


@router.post("")
@router.post("/")
async def add_patient(
    patient: PatientCreate,
    current_user=Depends(
        require_roles(
            "admin",
            "receptionist"
        )
    )
):
    return await create_patient(patient)

@router.get("/{patient_id}")
async def fetch_patient(
    patient_id: str,
    current_user=Depends(
        require_roles(
            "admin",
            "doctor",
            "receptionist"
        )
    )
):
    return await get_patient(patient_id)

@router.get("")
@router.get("/")
async def fetch_all_patients(
    current_user=Depends(
        require_roles(
            "admin",
            "doctor",
            "receptionist"
        )
    )
):
    return await get_all_patients()

from app.services.patient_service import update_patient

@router.put("/{patient_id}")
async def edit_patient(
    patient_id: str,
    patient: PatientCreate,
    current_user=Depends(
        require_roles(
            "admin",
            "receptionist"
        )
    )
):
    return await update_patient(
        patient_id,
        patient
    )

from app.services.patient_service import delete_patient

@router.delete("/{patient_id}")
async def remove_patient(
    patient_id: str,
    current_user=Depends(
        require_roles(
            "admin"
        )
    )
):
    return await delete_patient(patient_id)