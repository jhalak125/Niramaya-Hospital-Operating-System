import json

from app.ai.groq_service import client


async def generate_english_narration(report):

    prompt = f"""
You are Vaidya AI.

Explain this report naturally.

Speak like a caring doctor.

Do NOT read JSON fields.

Use simple English.

Explain:

• what was found
• whether it is serious
• lifestyle suggestions
• questions to ask doctor

End with:

Please remember that this explanation is only for educational purposes and is not a medical diagnosis.

Medical Report:

{json.dumps(report, indent=2)}
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

    return response.choices[0].message.content


async def generate_hindi_narration(report):

    prompt = f"""
You are Vaidya AI.

Explain this medical report in simple spoken Hindi.

Rules:

Speak naturally.

Avoid difficult Sanskrit.

Avoid English wherever possible.

Explain like a friendly Indian doctor.

End with:

ध्यान रखें कि यह केवल आपकी जानकारी के लिए है। कृपया अपने डॉक्टर से अवश्य परामर्श करें।

Medical Report:

{json.dumps(report, indent=2)}
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

    return response.choices[0].message.content