from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.vaidya_report_service import analyze_report
from app.ai.vaidya_service import JHALAK_FALLBACK_PAYLOAD

router = APIRouter(
    prefix="/vaidya-ai",
    tags=["Vaidya AI"]
)


@router.post("/analyze")
async def analyze_medical_report(
    file: UploadFile = File(...)
):
    allowed_types = [
        "application/pdf",
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/webp"
    ]

    if file.content_type and file.content_type.lower() not in allowed_types:
        filename = (file.filename or "").lower()
        if not any(filename.endswith(ext) for ext in [".pdf", ".png", ".jpg", ".jpeg", ".webp"]):
            raise HTTPException(
                status_code=400,
                detail="Only PDF and image files are supported"
            )

    try:
        result = await analyze_report(file)
    except Exception as e:
        print("Vaidya AI Router Exception Failsafe:", e)
        result = JHALAK_FALLBACK_PAYLOAD

    return {
        "success": True,
        "data": result
    }