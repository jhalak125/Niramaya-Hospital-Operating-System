import json

from app.ai.groq_service import client


async def generate_english_narration(report):

    prompt = f"""
You are Vaidya AI, a compassionate medical doctor.

Below is the clinical evaluation of a patient's printed diagnostic report:

{json.dumps(report, indent=2)}

INSTRUCTIONS:
1. Explain all the diagnostic findings, organ measurements, impressions, and lab results in simple, reassuring layman language.
2. Speak naturally and warmly like a friendly doctor explaining the report directly to the patient during a consultation.
3. DO NOT use headings (like "What was found:", "Is it serious:", "Lifestyle suggestions:", "Questions to ask your doctor:").
4. DO NOT use colons, robotic bullet titles, or formal section dividers.
5. Flow smoothly from explaining the organ findings, to what they mean, to practical daily advice, and guidance for their doctor visit.
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

    return response.choices[0].message.content


async def generate_hindi_narration(report):

    prompt = f"""
आप वैद्य AI (Vaidya AI) हैं, एक संवेदनशील और अनुभवी डॉक्टर।

नीचे मरीज की मेडिकल रिपोर्ट का विवरण दिया गया है:

{json.dumps(report, indent=2)}

नियम (INSTRUCTIONS):
1. रिपोर्ट की सभी बातों, अंगों की स्थिति और निष्कर्षों को बेहद सरल हिंदी में समझाएं।
2. जैसे एक डॉक्टर मरीज से आमने-सामने बैठकर प्यार से समझाता है, ठीक वैसे ही स्वाभाविक रूप से बोलें।
3. कोई रोबोटिक हेडिंग्स या कोलन (जैसे "क्या पाया गया:", "क्या यह गंभीर है:", "जीवनशैली:") का उपयोग बिल्कुल न करें।
4. बिल्कुल सरल, बोलचाल की हिंदी भाषा का प्रयोग करें।
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

    return response.choices[0].message.content