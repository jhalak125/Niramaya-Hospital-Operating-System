from fastapi import Depends, HTTPException

from app.auth.security import verify_token

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


async def get_current_user(
    token: str = Depends(oauth2_scheme)
):

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )

    return payload


async def require_admin(
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return current_user


async def require_doctor(
    current_user=Depends(get_current_user)
):

    if current_user["role"] != "doctor":
        raise HTTPException(
            status_code=403,
            detail="Doctor access required"
        )

    return current_user

async def require_patient(current_user=Depends(get_current_user)):
    if current_user["role"] != "patient":
        raise HTTPException(
            status_code=403,
            detail="Patient access required"
        )
    return current_user


async def require_admin_or_doctor(
    current_user=Depends(get_current_user)
):

    if current_user["role"] not in ["admin", "doctor"]:
        raise HTTPException(
            status_code=403,
            detail="Access denied"
        )

    return current_user