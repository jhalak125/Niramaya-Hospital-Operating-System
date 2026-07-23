from fastapi import APIRouter
from app.schemas.ai_schema import SymptomRequest
from app.ai.gemini_service import analyze_symptoms

router = APIRouter(
    prefix="/ai",
    tags=["AI Assistant"]
)


@router.post("/symptom-check")
async def symptom_checker(
    request: SymptomRequest
):
    result = await analyze_symptoms(
        request.symptoms
    )

    return {
        "analysis": result
    }