from groq import Groq
import json

client = Groq(api_key="your-groq-api-key-here")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
       {
            "role": "system",
            "content": """You are Dr. Emeka, a senior emergency physician 
            with 20 years of experience in prehospital trauma care in Nigeria. 
            You speak directly, use clinical language, and always prioritise 
            life-threatening conditions first. You are training junior paramedics."""
        },
        {
            "role": "user",
            "content": "A motorcyclist was hit by a car. He is conscious but confused, has a deformed left leg and is bleeding heavily. What do I do?"
        }
    ]
)

print(response.choices[0].message.content)