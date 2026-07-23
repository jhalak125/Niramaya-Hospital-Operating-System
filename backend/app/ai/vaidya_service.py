import json

from app.ai.groq_service import client


async def analyze_medical_report(report_text: str):

    prompt = f"""
You are Vaidya AI.

Below is the extracted OCR text from a medical report.

{report_text}

Return ONLY JSON.

{{
"summary":"",
"report_type":"",
"abnormal_findings":[],
"layman_explanation":"",
"lifestyle_suggestions":[],
"questions_to_ask_doctor":[],
"severity":"Normal | Mild | Moderate | Urgent",
"hindi_explanation":"",
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
        ]

    )

    text = response.choices[0].message.content

    if text.startswith("```"):
        text = (
            text.replace("```json", "")
                .replace("```", "")
                .strip()
        )

    return json.loads(text)