from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
import os
import json

load_dotenv()

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define what data the endpoint expects
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
def triage(patient: Patient):
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
                    "content": f"Patient data: {patient}, Age: {patient.age}, Symptoms: {patient.symptoms}"
                }
            ]
        )
    
    import json
    result = json.loads(response.choices[0].message.content)
    
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

@app.get("/severity/{level}")
def severity_guide(level: str):
    guides = {
        "CRITICAL": "Immediate life-threatening — call emergency services now",
        "URGENT": "Serious condition — seek medical attention within 1 hour",
        "STABLE": "Non-life-threatening — monitor and seek care when possible"
    }
    level = level.upper()
    if level not in guides:
        return {"error": "Invalid severity level. Use CRITICAL, URGENT, or STABLE"}
    return {"severity": level, "guidance": guides[level]}