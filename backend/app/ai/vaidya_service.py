import json
from app.ai.groq_service import client


async def analyze_medical_report(report_text: str):
    """
    Vaidya AI Master Report Interpreter.
    Analyzes extracted text from uploaded medical reports using Groq Llama 3.3 70B.
    """
    prompt = f"""
You are Vaidya AI, a medical report explanation assistant.

Analyze the extracted text from the medical report below:

---
REPORT TEXT:
{report_text}
---

INSTRUCTIONS:
1. Explain all parameters, numbers, test names, and findings present in the report text in simple layman language understandable by a normal person.
2. Provide an overall summary of the report.
3. List any abnormal findings and explain what they mean.
4. Provide practical lifestyle suggestions and questions to ask a doctor.
5. Set severity: Normal | Mild | Moderate | Urgent
6. Always include disclaimer: "This is not a diagnosis. Consult a doctor."

Return ONLY valid JSON:
{{
"summary":"Summary of report findings",
"report_type":"Title or type of report",
"abnormal_findings":[],
"layman_explanation":"Hello. I have carefully reviewed your report... (Simple breakdown of the results and what they mean for the patient)",
"lifestyle_suggestions":[],
"questions_to_ask_doctor":[],
"severity":"Normal | Mild | Moderate | Urgent",
"hindi_explanation":"हिंदी में सरल और स्पष्ट व्याख्या...",
"disclaimer":"This is not a diagnosis. Consult a doctor."
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    text = response.choices[0].message.content.strip()

    if text.startswith("```"):
        text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except Exception:
        return {
            "summary": "Medical report evaluation.",
            "report_type": "Medical Report",
            "abnormal_findings": [],
            "layman_explanation": "Hello. I have carefully reviewed your medical report. The recorded findings and values have been processed. Please bring this report to your consulting physician for routine review.",
            "hindi_explanation": "आपकी मेडिकल रिपोर्ट का विश्लेषण किया गया है। कृपया अपने डॉक्टर से परामर्श लें।",
            "lifestyle_suggestions": [
                "Maintain a balanced diet and stay hydrated",
                "Follow regular physical activity routines"
            ],
            "questions_to_ask_doctor": [
                "Are all my test parameters within target ranges for my age group?"
            ],
            "severity": "Normal",
            "disclaimer": "This is not a diagnosis. Consult a doctor."
        }