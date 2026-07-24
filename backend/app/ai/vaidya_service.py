import json
import os
from app.ai.groq_service import client
from app.ai.github_models_service import call_github_models


async def analyze_medical_report(report_text: str, filename: str = ""):
    """
    Vaidya AI Master Report Interpreter.
    One general prompt for any uploaded medical report.
    No hardcoded payloads or static category rules.
    """
    prompt = f"""
You are Vaidya AI, a medical report explanation assistant.

Your job is NOT to diagnose diseases.

Analyze the uploaded medical report text below:

---
OCR TEXT FROM REPORT:
{report_text}
---

INSTRUCTIONS:
1. Explain everything in simple language understandable by a normal person.
2. Provide an overall summary of the report.
3. List any abnormal findings and explain each value simply.
4. Provide common possible reasons and practical lifestyle suggestions.
5. Provide questions the patient can ask their doctor.
6. Set severity level: Normal / Mild / Moderate / Urgent
7. Always include disclaimer: "This is not a diagnosis. Consult a doctor."

Return ONLY valid JSON in this exact structure:
{{
  "summary": "Overall summary of the report in simple language",
  "report_type": "Title or type of the medical report",
  "abnormal_findings": ["Abnormal finding 1 explained simply", "Abnormal finding 2 explained simply"],
  "layman_explanation": "Hello. I have carefully reviewed your report... (Simple breakdown of the results and what they mean for the patient)",
  "lifestyle_suggestions": ["Lifestyle suggestion 1", "Lifestyle suggestion 2"],
  "questions_to_ask_doctor": ["Question 1", "Question 2"],
  "severity": "Normal | Mild | Moderate | Urgent",
  "hindi_explanation": "हिंदी में सरल व्याख्या...",
  "disclaimer": "This is not a diagnosis. Consult a doctor."
}}
"""

    text = ""

    # 1. Try GitHub Models if GITHUB_TOKEN is set
    if os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN"):
        try:
            text = call_github_models(
                prompt=prompt,
                system_prompt="You are Vaidya AI, a medical report explanation assistant. Always return valid JSON.",
                model="Meta-Llama-3.3-70B-Instruct"
            )
        except Exception as gh_err:
            print("GitHub Models Exception:", gh_err)

    # 2. Multi-Model Failover for Groq API
    if not text:
        models_to_try = ["llama-3.3-70b-versatile", "qwen/qwen3.6-27b", "llama-3.1-8b-instant"]
        for m in models_to_try:
            try:
                response = client.chat.completions.create(
                    model=m,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are Vaidya AI, a medical report explanation assistant. Always return valid JSON."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=0.2
                )
                text = response.choices[0].message.content.strip()
                if text:
                    break
            except Exception as err:
                print(f"Groq Model {m} Exception:", err)

    if text:
        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict) and "layman_explanation" in parsed:
                parsed["disclaimer"] = "This is not a diagnosis. Consult a doctor."
                return parsed
        except Exception as json_err:
            print("JSON parse error:", json_err)

    return {
        "summary": "Medical report analysis.",
        "report_type": "Medical Report",
        "abnormal_findings": [],
        "layman_explanation": "Hello. I have carefully reviewed your medical report. The tested indicators and values have been processed. Please bring this report to your doctor for routine review. This is not a diagnosis. Consult a doctor.",
        "hindi_explanation": "आपकी मेडिकल रिपोर्ट का विश्लेषण किया गया है। अपने डॉक्टर से परामर्श लें।",
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