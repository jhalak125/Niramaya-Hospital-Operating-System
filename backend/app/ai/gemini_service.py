import os
import json
from groq import Groq
from dotenv import load_dotenv
from app.services.doctor_service import get_department_doctors
from app.utils.department_mapper import map_department

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


async def analyze_symptoms(symptoms: str):

    prompt = f"""
You are an experienced medical triage assistant.

A patient reports the following symptoms:

{symptoms}

Return ONLY valid JSON.

{{
    "possible_conditions":[
        "condition1",
        "condition2",
        "condition3"
    ],
    "recommended_department":"",
    "urgency":"Low | Medium | High | Emergency",
    "advice":"",
    "recommended_tests":[
        "test1",
        "test2"
    ],
    "precautions":[
        "precaution1",
        "precaution2"
    ],
    "disclaimer":"This is not a medical diagnosis. Consult a qualified doctor."
}}
"""

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "system",
            "content": "You are an experienced medical triage assistant."
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
        text = text.replace("```json", "").replace("```", "").strip()

    result = json.loads(text)

    department = result.get("recommended_department")

    print("AI:", department)

    mapped_department = map_department(department)

    print("Mapped:", mapped_department)

    doctors = await get_department_doctors(mapped_department)

    print("Doctors:", doctors)

    result["available_doctors"] = doctors

    if result["urgency"].lower().startswith("emergency"):

        result["next_step"] = (
            "Visit the Emergency Department immediately."
        )

    elif doctors:

        result["next_step"] = (
            "Book an appointment with one of the available doctors."
        )

    else:

        result["next_step"] = (
            "No doctors are currently available. Please contact the hospital."
        )
    return result