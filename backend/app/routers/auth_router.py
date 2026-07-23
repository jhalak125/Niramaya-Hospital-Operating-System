from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserRegister
from app.services.auth_service import (
    get_user_by_email,
    create_user
)
from app.schemas.user_schema import UserLogin
from app.services.auth_service import login_user
from app.dependencies.auth_dependency import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from app.dependencies.role_dependency import require_roles
from app.auth.google_auth import verify_google_token
from app.schemas.google_schema import GoogleLogin
from app.repositories.user_repository import UserRepository
from app.auth.security import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
async def register(user: UserRegister):

    existing_user = await get_user_by_email(user.email)

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
        )

    user_id = await create_user(user)

    return {
        "message": "User registered successfully",
        "user_id": str(user_id)
    }

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    token = await login_user(
        form_data.username,
        form_data.password
    )

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.get("/me")
async def get_me(

    current_user = Depends(get_current_user)

):

    return current_user

@router.get("/admin-dashboard")
async def admin_dashboard(
    current_user=Depends(
        require_roles("admin")
    )
):

    return {
        "message": "Welcome Admin",
        "user": current_user
    }

@router.get("/doctor-dashboard")
async def doctor_dashboard(
    current_user=Depends(
        require_roles("doctor")
    )
):

    return {
        "message":"Welcome Doctor"
    }

@router.get("/appointments/manage")
async def manage_appointments(
    current_user=Depends(
        require_roles(
            "admin",
            "receptionist"
        )
    )
):

    return {
        "message":"Appointment Management"
    }

@router.post("/google-login")
async def google_login(data: GoogleLogin):

    google_user = verify_google_token(data.token)

    if google_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Google Token"
        )

    email = google_user["email"]
    name = google_user["name"]

    user = await UserRepository.get_by_email(email)

    if user is None:
        user = await UserRepository.create_google_user(
            email=email,
            name=name
        )

    access_token = create_access_token(
        {
            "sub": str(user["_id"]),
            "email": user["email"],
            "role": user["role"]
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": str(user["_id"]),
            "name": user.get("name") or user.get("full_name") or name,
            "email": user["email"],
            "role": user["role"]
        }
    }