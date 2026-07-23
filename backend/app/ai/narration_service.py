import json
import re
from app.ai.groq_service import client


def _clean_narrative(text: str) -> str:
    if not text:
        return ""
    # Strip robotic heading titles like "What was found:", "Is it serious:", "Lifestyle suggestions:", "Questions to ask your doctor:"
    cleaned = re.sub(r'^(What was found|Is it serious|Lifestyle suggestions|Questions to ask your doctor|Summary|Findings|Severity|Advice)\s*:?\s*', '', text, flags=re.MULTILINE | re.IGNORECASE)
    # Strip any line consisting of a title ending with a colon
    cleaned = re.sub(r'^[A-Z][a-zA-Z\s]{1,35}:\s*$', '', cleaned, flags=re.MULTILINE)
    # Strip bullet stars/dashes at line starts
    cleaned = re.sub(r'^\s*[\*\-\•]\s*', '', cleaned, flags=re.MULTILINE)
    lines = [line.strip() for line in cleaned.split('\n') if line.strip()]
    return '\n\n'.join(lines)


async def generate_english_narration(report):

    prompt = f"""
You are Dr. Vaidya, a senior compassionate medical doctor and radiologist.

Below is the clinical evaluation of a patient's medical diagnostic report:

{json.dumps(report, indent=2)}

MANDATORY STYLE RULES:
1. Speak warmly, clearly, and naturally like an experienced doctor sitting across the desk explaining the report directly to the patient during a consultation.
2. Output ONLY plain, continuous narrative paragraphs.
3. FORBIDDEN: Do NOT use any headings, titles, section names, colons, bullet points, numbered lists, or section labels anywhere in your text.
4. Explain every single finding, organ measurement, lab value, and impression in simple everyday layman language line by line.
5. Flow smoothly from explaining the organ findings, to what they mean, to practical daily advice, and guidance for their doctor visit as part of the natural spoken explanation.
6. End with: "Please remember that this explanation is for educational purposes and is not a substitute for formal clinical diagnosis."
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    raw_text = response.choices[0].message.content
    return _clean_narrative(raw_text)


async def generate_hindi_narration(report):

    prompt = f"""
आप डॉ. वैद्य (Dr. Vaidya) हैं, एक संवेदनशील और अनुभवी वरिष्ठ डॉक्टर।

नीचे मरीज की मेडिकल रिपोर्ट का विवरण दिया गया है:

{json.dumps(report, indent=2)}

नियम (INSTRUCTIONS):
1. रिपोर्ट की सभी बातों, अंगों की स्थिति और निष्कर्षों को बेहद सरल, बोलचाल की हिंदी में समझाएं।
2. जैसे एक डॉक्टर मरीज से आमने-सामने बैठकर प्यार से समझाता है, ठीक वैसे ही स्वाभाविक रूप से बोलें।
3. किसी भी प्रकार की रोबोटिक हेडिंग, शीर्षक, या कोलन (जैसे "क्या पाया गया:", "क्या यह गंभीर है:", "जीवनशैली:") का उपयोग बिल्कुल न करें।
4. केवल सीधे संवाद पैराग्राफ में उत्तर दें।
5. अंत में कहें: "ध्यान रखें कि यह जानकारी केवल आपकी समझ के लिए है। कृपया अपने डॉक्टर से परामर्श अवश्य लें।"
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    raw_text = response.choices[0].message.content
    return _clean_narrative(raw_text)