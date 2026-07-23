import json

from app.ai.groq_service import client


async def analyze_medical_report(report_text: str):

    prompt = f"""
You are Vaidya AI, an expert medical report interpreter and compassionate clinical assistant.

Below is the extracted text from a medical report (Sonography / Ultrasound, Blood Test, X-Ray, CT Scan, MRI, Pathology, or Diagnostic Report):

---
{report_text}
---

INSTRUCTIONS FOR LAYMAN EXPLANATION:
1. Explain every clinical finding, organ measurement, impression, and diagnostic observation in simple, easy-to-understand everyday language.
2. Break down medical jargon into simple terms (e.g. 'hepatomegaly' -> 'mild enlargement of the liver', 'cholelithiasis' -> 'gallstones in the gallbladder', 'echogenic' -> 'tissue density on ultrasound').
3. Explain clearly whether findings are normal, borderline, or require doctor consultation.
4. Provide practical, compassionate lifestyle suggestions tailored to the specific findings.
5. Provide actionable questions the patient can ask their doctor.
6. NEVER say 'no report provided' or give generic empty responses.

Return ONLY valid JSON matching this exact structure:
{{
  "summary": "Clear 2-3 sentence overview of the report findings",
  "report_type": "Sonography / Ultrasound / Blood Test / Radiology Report",
  "abnormal_findings": ["Finding 1 with explanation", "Finding 2 with explanation"],
  "layman_explanation": "Detailed, step-by-step breakdown of the report findings in simple, easy-to-understand layman language...",
  "lifestyle_suggestions": ["Specific practical health suggestion 1", "Specific practical health suggestion 2"],
  "questions_to_ask_doctor": ["What does this finding mean for my daily health?", "Do I need any follow-up ultrasound scan or test?"],
  "severity": "Normal | Mild | Moderate | Urgent",
  "hindi_explanation": "Comprehensive explanation of findings in clear, simple Hindi (हिंदी विवरण)...",
  "disclaimer": "This explanation is for educational understanding only and is not a substitute for professional medical diagnosis. Please consult a qualified doctor."
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are Vaidya AI, an expert medical report interpreter. Always return structured JSON with detailed, simple layman explanations of diagnostic findings."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    text = response.choices[0].message.content.strip()

    if text.startswith("```"):
        text = (
            text.replace("```json", "")
                .replace("```", "")
                .strip()
        )

    return json.loads(text)