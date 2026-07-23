from datetime import datetime
from app.database.database import db
from app.auth.security import hash_password
from app.auth.security import verify_password, create_access_token
from app.services.audit_log_service import create_audit_log


async def get_user_by_email(email: str):
    if not email:
        return None
    clean_email = email.strip()
    return await db.users.find_one({"email": {"$regex": f"^{clean_email}$", "$options": "i"}})


async def create_user(user):
    user_data = {
        "full_name": user.full_name,
        "email": user.email.strip().lower(),
        "password": hash_password(user.password),
        "phone": user.phone,
        "role": user.role,
        "is_active": True,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = await db.users.insert_one(user_data)

    await create_audit_log(
        user_id=str(result.inserted_id),
        action="CREATE",
        module="USER",
        module_id=str(result.inserted_id),
        description=f"New user {user.email} registered"
    )

    return result.inserted_id

async def login_user(email: str, password: str):
    user = await get_user_by_email(email)

    if not user:
        return None

    hashed_pwd = user.get("password")
    if not hashed_pwd or not verify_password(password, hashed_pwd):
        return None

    token = create_access_token(
        {
            "sub": str(user["_id"]),
            "email": user["email"],
            "role": user["role"]
        }
    )

    await create_audit_log(
        user_id=str(user["_id"]),
        action="LOGIN",
        module="USER",
        module_id=str(user["_id"]),
        description=f"{user['email']} logged into the system"
    )

    return token