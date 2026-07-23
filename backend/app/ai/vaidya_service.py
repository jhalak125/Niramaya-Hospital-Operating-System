import json

from app.ai.groq_service import client


async def analyze_medical_report(report_text: str):

    prompt = f"""
You are Vaidya AI, an expert medical report interpreter and compassionate clinical assistant.

Below is the extracted text from a medical diagnostic report (Sonography / Ultrasound, Blood Test, X-Ray, CT Scan, MRI, Pathology, or Clinical Lab Report):

---
{report_text}
---

MANDATORY INSTRUCTIONS FOR CLINICAL ANALYSIS:
1. Thoroughly analyze all patient details, diagnostic findings, organ measurements, lab values, and clinical impressions in the report.
2. Write a warm, clear, conversational doctor-to-patient narrative in simple layman language that explains all findings line by line.
3. DO NOT use robotic section titles or headings like "What was found:", "Is it serious:", "Lifestyle suggestions:", or "Questions to ask your doctor:".
4. DO NOT use colons, bullet labels, or formal section dividers in the explanation. Write fluidly like a caring doctor speaking naturally to a patient in consultation.
5. Translate all clinical jargon into simple words (e.g. 'Polycystic sonomorphology' -> 'Ovaries displaying multiple tiny fluid-filled follicles', 'Endometrium' -> 'Inner lining of the uterus', 'Anteverted' -> 'Normally tilted forward').
6. Provide reassuring guidance, daily health suggestions, and advice for their doctor visit seamlessly within the narrative.

Return ONLY valid JSON matching this exact structure:
{{
  "summary": "Clear 2-3 sentence overview of the report findings",
  "report_type": "Sonography / Ultrasound / Blood Test / Radiology Report",
  "abnormal_findings": ["Finding 1 with explanation", "Finding 2 with explanation"],
  "layman_explanation": "Warm, conversational doctor-to-patient narrative explaining all findings line by line in simple everyday language...",
  "lifestyle_suggestions": ["Specific practical health suggestion 1", "Specific practical health suggestion 2"],
  "questions_to_ask_doctor": ["What does this finding mean for my daily health?", "Do I need any follow-up ultrasound scan or test?"],
  "severity": "Normal | Mild | Moderate | Urgent",
  "hindi_explanation": "हिंदी में डॉक्टर-मरीज बातचीत शैली में सरल व्याख्या...",
  "disclaimer": "This explanation is for educational understanding only and is not a substitute for formal clinical diagnosis. Please consult a qualified doctor."
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