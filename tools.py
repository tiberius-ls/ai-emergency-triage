from groq import Groq
import json

client = Groq(api_key="your-groq-api-key-here")

# Step 1 — Define the tool
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_drug_dose",
            "description": "Calculates the correct drug dose based on patient weight",
            "parameters": {
                "type": "object",
                "properties": {
                    "drug_name": {
                        "type": "string",
                        "description": "Name of the drug"
                    },
                    "weight_kg": {
                        "type": "number",
                        "description": "Patient weight in kilograms"
                    },
                    "dose_per_kg": {
                        "type": "number",
                        "description": "Dose in mg per kg of body weight"
                    }
                },
                "required": ["drug_name", "weight_kg", "dose_per_kg"]
            }
        }
    }
]

# Step 2 — The actual function
def calculate_drug_dose(drug_name, weight_kg, dose_per_kg):
    total_dose = weight_kg * dose_per_kg
    return f"{drug_name}: {total_dose}mg for a {weight_kg}kg patient"

# Step 3 — Send message with tools
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are an emergency medicine assistant that calculates drug doses."
        },
        {
            "role": "user",
            "content": "Calculate the adrenaline dose for a 70kg patient. Dose is 0.01mg per kg."
        }
    ],
    tools=tools,
    tool_choice="auto"
)

# Step 4 — Check if AI wants to use a tool
message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)
    
    print("AI decided to use tool:", tool_call.function.name)
    print("With arguments:", args)
    
    # Step 5 — Run the actual function
    result = calculate_drug_dose(**args)
    print("Tool result:", result)


# Step 6 — Send tool result back to AI
final_response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": "You are an emergency medicine assistant that calculates drug doses."
        },
        {
            "role": "user",
            "content": "Calculate the adrenaline dose for a 70kg patient. Dose is 0.01mg per kg."
        },
        {
            "role": "assistant",
            "tool_calls": [
                {
                    "id": tool_call.id,
                    "type": "function",
                    "function": {
                        "name": tool_call.function.name,
                        "arguments": tool_call.function.arguments
                    }
                }
            ]
        },
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        }
    ],
    tools=tools
)

print("\nFinal AI Response:")
print(final_response.choices[0].message.content)