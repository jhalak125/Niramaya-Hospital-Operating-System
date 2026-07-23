import json
import re
from app.ai.groq_service import client


def _clean_narrative(text: str) -> str:
    if not text:
        return ""
    cleaned = re.sub(r'^(What was found|Is it serious|Lifestyle suggestions|Questions to ask your doctor|Summary|Findings|Severity|Advice)\s*:?\s*', '', text, flags=re.MULTILINE | re.IGNORECASE)
    cleaned = re.sub(r'^[A-Z][a-zA-Z\s]{1,35}:\s*$', '', cleaned, flags=re.MULTILINE)
    cleaned = re.sub(r'^\s*[\*\-\•]\s*', '', cleaned, flags=re.MULTILINE)
    lines = [line.strip() for line in cleaned.split('\n') if line.strip()]
    return '\n\n'.join(lines)


async def analyze_medical_report(report_text: str):

    prompt = f"""
You are Dr. Vaidya, an experienced senior medical doctor and clinical radiologist consulting directly with patient Miss Jhalak Verma.

Below is the text extracted from a patient's printed medical report:

---
{report_text}
---

MANDATORY INSTRUCTIONS FOR CLINICAL ANALYSIS:
1. Thoroughly analyze all patient details, diagnostic findings, organ measurements, lab values, and clinical impressions in the report.
2. Write a warm, clear, conversational doctor-to-patient narrative in simple layman language that explains all findings line by line.
3. FORBIDDEN: Do NOT use any headings, titles, section names, colons, bullet points, numbered lists, or section labels anywhere in your text.
4. Output plain, continuous narrative paragraphs as if speaking naturally to a patient in consultation.
5. Translate all clinical jargon into simple words (e.g. 'Polycystic sonomorphology' -> 'Ovaries displaying multiple tiny fluid-filled follicles', 'Endometrium' -> 'Inner lining of the uterus', 'Anteverted' -> 'Normally tilted forward').
6. Provide reassuring guidance, daily health suggestions, and advice for their doctor visit seamlessly within the narrative.
7. NEVER output 'No diagnosis provided', 'No abnormal findings', or 'nothing out of the ordinary' if the text contains sonography or clinical findings. You MUST extract and explain the organ dimensions, uterine cavity, endometrial thickness, cervical features, ovarian size/follicle count, and impression in detail.

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
                "content": "You are Dr. Vaidya, an expert medical report interpreter. Always return structured JSON with detailed, simple layman explanations of diagnostic findings."
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

    parsed = json.loads(text)
    if isinstance(parsed, dict) and "layman_explanation" in parsed:
        parsed["layman_explanation"] = _clean_narrative(parsed["layman_explanation"])
    return parsed