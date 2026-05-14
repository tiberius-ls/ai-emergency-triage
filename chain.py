from groq import Groq
import json

client = Groq(api_key="your-groq-api-key-here")

def ask(system, user):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user}
        ]
    )
    return response.choices[0].message.content

# Raw input
symptoms = "35-year-old male, sudden severe headache, stiff neck, fever, sensitivity to light"

# Step 1 — Diagnosis
diagnosis_raw = ask(
    """You are an emergency physician. 
    Respond in valid JSON only with these fields:
    {
        "condition": "diagnosis name",
        "severity": "CRITICAL, URGENT, or STABLE",
        "confidence": "HIGH, MEDIUM, or LOW"
    }""",
    f"Symptoms: {symptoms}"
)

diagnosis = json.loads(diagnosis_raw)
print("STEP 1 - STRUCTURED DIAGNOSIS:")
print(json.dumps(diagnosis, indent=2))
print()

# Step 2 — Treatment plan
treatment = ask(
    "You are an emergency physician. Give a treatment plan for this diagnosis.",
    f"Diagnosis: {diagnosis}"
)
print("STEP 2 - TREATMENT PLAN:")
print(treatment)
print()

# Step 3 — Patient summary
summary = ask(
    "You are a medical communicator. Explain this treatment plan in simple terms a non-medical person can understand.",
    f"Treatment plan: {treatment}"
)
print("STEP 3 - PATIENT SUMMARY:")
print(summary)