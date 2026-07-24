import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from app.services.doctor_service import get_department_doctors
from app.utils.department_mapper import map_department

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def _get_fallback_symptom_result(symptoms: str) -> dict:
    s_lower = (symptoms or "").lower()

    if any(k in s_lower for k in ["chest", "heart", "cardio", "breathless", "palpitation"]):
        return {
            "possible_conditions": [
                "Chest Muscle Strain / Intercostal Pain",
                "Gastroesophageal Reflux / Heartburn",
                "Mild Cardiovascular Evaluation Indicated"
            ],
            "recommended_department": "Cardiology",
            "urgency": "High",
            "advice": "Rest immediately in a comfortable posture. Avoid physical exertion and seek clinical evaluation by a cardiologist.",
            "recommended_tests": ["ECG / Electrocardiogram", "Troponin I Level", "Chest X-Ray"],
            "precautions": ["Avoid strenuous physical exercise", "Avoid heavy oily meals", "Monitor blood pressure and pulse"]
        }

    if any(k in s_lower for k in ["fever", "chill", "temperature", "body pain", "flu", "cough"]):
        return {
            "possible_conditions": [
                "Viral Pyrexia",
                "Upper Respiratory Tract Infection",
                "Seasonal Influenza"
            ],
            "recommended_department": "General Medicine",
            "urgency": "Medium",
            "advice": "Ensure plenty of rest, maintain hydration with fluids and warm water, and monitor body temperature.",
            "recommended_tests": ["Complete Blood Count (CBC)", "Inflammatory Markers (CRP)", "Viral Fever Panel"],
            "precautions": ["Drink 2-3 liters of fluids daily", "Rest adequately", "Use lukewarm sponge for body temperature"]
        }

    if any(k in s_lower for k in ["stomach", "abdominal", "pelvic", "ovary", "cramp", "period", "pcos", "pcod"]):
        return {
            "possible_conditions": [
                "Polycystic Ovarian Sonomorphology / PCOD",
                "Dysmenorrhea / Pelvic Cramping",
                "Functional Ovarian Cysts"
            ],
            "recommended_department": "Gynecology",
            "urgency": "Medium",
            "advice": "Maintain a low-glycemic balanced diet, engage in light daily exercise, and track your monthly cycle symptoms.",
            "recommended_tests": ["Pelvic Ultrasound Scan", "Serum Hormone Panel (FSH/LH)", "Routine Blood Examination"],
            "precautions": ["Maintain balanced nutrition", "Keep a daily symptom tracking log", "Avoid excessive physical stress"]
        }

    return {
        "possible_conditions": [
            "General Symptomatic Indisposition",
            "Mild Stress / Fatigue",
            "Routine Wellness Evaluation Needed"
        ],
        "recommended_department": "General Medicine",
        "urgency": "Low",
        "advice": "Stay hydrated, maintain healthy sleep habits, and consult a physician for routine health evaluation.",
        "recommended_tests": ["Basic Metabolic Panel", "Complete Blood Count"],
        "precautions": ["Stay well-hydrated", "Ensure 7-8 hours of sleep", "Eat fresh balanced meals"]
    }


async def analyze_symptoms(symptoms: str):
    prompt = f"""
You are an experienced medical triage assistant.

A patient reports the following symptoms:

{symptoms}

Return ONLY valid JSON with this exact structure:

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

    result = None

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "system",
                    "content": "You are an experienced medical triage assistant. Always return pure structured JSON."
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
            text = re.sub(r'^```(json)?\s*', '', text, flags=re.IGNORECASE)
            text = re.sub(r'\s*```$', '', text)

        result = json.loads(text)
    except Exception as e:
        print("Symptom Checker Groq/Parsing Exception:", e)
        result = _get_fallback_symptom_result(symptoms)

    if not isinstance(result, dict) or "recommended_department" not in result:
        result = _get_fallback_symptom_result(symptoms)

    result["disclaimer"] = "This is not a medical diagnosis. Consult a qualified doctor."

    department = result.get("recommended_department", "General Medicine")
    mapped_department = map_department(department)

    try:
        doctors = await get_department_doctors(mapped_department)
    except Exception as doc_err:
        print("Get Department Doctors Exception:", doc_err)
        doctors = []

    result["available_doctors"] = doctors

    urgency = str(result.get("urgency", "Low")).lower()

    if urgency.startswith("emergency"):
        result["next_step"] = "Visit the Emergency Department immediately."
    elif doctors:
        result["next_step"] = "Book an appointment with one of the available doctors."
    else:
        result["next_step"] = "No doctors are currently available for this specialty online. Please contact the hospital helpdesk."

    return result