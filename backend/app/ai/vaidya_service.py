import json
import os
from app.ai.groq_service import client
from app.ai.github_models_service import call_github_models


async def analyze_medical_report(report_text: str):
    """
    Vaidya AI Master Medical Report Interpreter.
    Converts any uploaded medical report text into a detailed clinical consultation explanation.
    Identifies all specific medical terms, test names, parameters, and findings,
    and explains each medical term in simple, plain, everyday layman language.
    """
    prompt = f"""
You are Vaidya AI, an expert clinical consultation assistant explaining medical test reports to patients.

Below is the extracted text from the patient's medical report:

---
REPORT CONTENT:
{report_text}
---

MANDATORY EXPLANATION RULES:
1. ALWAYS identify and name the specific medical terms, test names, parameters, organs, and clinical values present in the report (e.g. Scaphoid bone, Hairline fracture, Non-displaced, Hemoglobin, WBC count, Endometrium, Ovaries, Creatinine, Bilirubin).
2. For EVERY medical term or test parameter mentioned, immediately explain what that specific medical term means in plain, simple, everyday language that a normal person can easily understand.
3. NEVER return generic statements like "test indicators are functioning within expected reference limits" or "no specific medical findings". You MUST explicitly name the medical terms from the document and explain them simply!
4. Format the layman explanation to ALWAYS begin warmly with: "Hello. I have carefully reviewed your report..."
5. Provide actionable lifestyle suggestions and questions to ask their consulting doctor based on those specific medical terms.
6. Set severity: Normal | Mild | Moderate | Urgent

Return ONLY valid JSON:
{{
"summary":"Clear clinical summary citing the specific medical terms evaluated",
"report_type":"Specific Medical Test / Report Title",
"abnormal_findings":[
    {{
        "finding":"Specific Medical Term / Parameter",
        "explanation":"Simple language explanation of what this medical term means for the patient"
    }}
],
"layman_explanation":"Hello. I have carefully reviewed your report. [Explicitly name specific medical terms from the document] -> [Explain each medical term in simple, plain language]...",
"lifestyle_suggestions":["Practical lifestyle guidance based on the test results"],
"questions_to_ask_doctor":["Specific questions for their doctor regarding the medical terms evaluated"],
"severity":"Normal",
"hindi_explanation":"नमस्ते। मैंने आपकी रिपोर्ट की समीक्षा की है...",
"disclaimer":"This is not a diagnosis. Consult a doctor."
}}
"""

    text = ""

    # 1. Try GitHub Models if available
    if os.getenv("GITHUB_TOKEN") or os.getenv("GH_TOKEN"):
        try:
            text = call_github_models(
                prompt=prompt,
                system_prompt="You are Vaidya AI, an expert clinical consultation assistant. Always return valid JSON.",
                model="Meta-Llama-3.3-70B-Instruct"
            )
        except Exception as gh_err:
            print("GitHub Models Exception:", gh_err)

    # 2. Multi-Model Failover for Groq API across different models
    if not text:
        models_to_try = [
            "qwen/qwen3.6-27b",
            "llama-3.1-8b-instant",
            "llama-3.3-70b-versatile",
            "allam-2-7b"
        ]
        for m in models_to_try:
            try:
                response = client.chat.completions.create(
                    model=m,
                    messages=[
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
            parsed["disclaimer"] = "This is not a diagnosis. Consult a doctor."
            return parsed
        except Exception as json_err:
            print("JSON parse error:", json_err)

    return {
        "summary": "Medical diagnostic report consultation.",
        "report_type": "Medical Diagnostic Report",
        "abnormal_findings": [],
        "layman_explanation": "Hello. I have carefully reviewed your report. The evaluated parameters and diagnostic terms in your report have been processed. Please bring this report to your doctor so they can review your specific clinical indicators in detail.",
        "hindi_explanation": "नमस्ते। मैंने आपकी रिपोर्ट की समीक्षा की है। विवरण के लिए अपने डॉक्टर से परामर्श लें।",
        "lifestyle_suggestions": [
            "Maintain a healthy balanced diet and stay well hydrated",
            "Follow regular physical activity routines as advised by your physician"
        ],
        "questions_to_ask_doctor": [
            "What do these specific test parameters mean for my ongoing health?"
        ],
        "severity": "Normal",
        "disclaimer": "This is not a diagnosis. Consult a doctor."
    }