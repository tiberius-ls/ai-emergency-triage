from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(key: str = Security(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return key

class Patient(BaseModel):
    name: str
    age: int
    symptoms: str

@app.get("/")
def home():
    return {"message": "AI Triage API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/triage")
def triage(patient: Patient, api_key: str = Security(verify_api_key)):
    # Validate age
    if patient.age <= 0 or patient.age > 120:
        raise HTTPException(
            status_code=400,
            detail="Invalid age. Must be between 1 and 120"
        )

    # Validate symptoms
    if len(patient.symptoms.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Please provide more detailed symptoms"
        )

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are an emergency triage assistant.
                    Respond in valid JSON only with these fields:
                    {
                        "condition": "most likely condition",
                        "severity": "CRITICAL, URGENT, or STABLE",
                        "immediate_action": "what to do now"
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Patient: {patient.name}, Age: {patient.age}, Symptoms: {patient.symptoms}"
                }
            ]
        )
        result = json.loads(response.choices[0].message.content)

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=500,
            detail="AI returned invalid response. Please try again"
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail="AI service temporarily unavailable. Please try again"
        )

    return {
        "patient": patient.name,
        "age": patient.age,
        "symptoms": patient.symptoms,
        "diagnosis": result
    }

class DrugDose(BaseModel):
    drug_name: str
    weight_kg: float
    dose_per_kg: float

@app.post("/drug-dose")
def drug_dose(data: DrugDose):
    total_dose = data.weight_kg * data.dose_per_kg
    return {
        "drug": data.drug_name,
        "patient_weight": f"{data.weight_kg}kg",
        "dose_per_kg": f"{data.dose_per_kg}mg/kg",
        "total_dose": f"{round(total_dose, 2)}mg"
    }

@app.get("/severity-info")
def severity_info(level: str = "STABLE", language: str = "english"):
    guides = {
        "CRITICAL": "Immediate life-threatening — call emergency services now",
        "URGENT": "Serious condition — seek medical attention within 1 hour",
        "STABLE": "Non-life-threatening — monitor and seek care when possible"
    }

    level = level.upper()

    if level not in guides:
        raise HTTPException(
            status_code=400,
            detail="Invalid severity. Use CRITICAL, URGENT, or STABLE"
        )

    return {
        "severity": level,
        "guidance": guides[level],
        "language": language,
        "emergency_number": "112" if language == "english" else "112"
    }