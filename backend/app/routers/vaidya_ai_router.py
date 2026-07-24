from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.vaidya_report_service import analyze_report


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
        "image/jpg"
    ]


    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and image files are supported"
        )


    result = await analyze_report(file)


    return {
        "success": True,
        "data": result
    }