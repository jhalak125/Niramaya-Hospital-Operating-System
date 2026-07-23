from datetime import datetime
from app.repositories.audit_log_repository import AuditLogRepository


async def create_audit_log(
    user_id: str,
    action: str,
    module: str,
    description: str,
    role: str = None,
    module_id: str = None,
    ip_address: str = None,
    old_values: dict = None,
    new_values: dict = None,
):
    log = {
        "user_id": user_id,
        "role": role,
        "action": action,
        "module": module,
        "module_id": module_id,
        "description": description,
        "ip_address": ip_address,
        "old_values": old_values,
        "new_values": new_values,
        "timestamp": datetime.utcnow(),
    }

    return await AuditLogRepository.create(log)


async def get_all_logs():
    logs = await AuditLogRepository.get_all()

    for log in logs:
        log["_id"] = str(log["_id"])

    return logs