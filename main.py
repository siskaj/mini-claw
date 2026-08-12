from openai import OpenAI
from tools import get_current_time

client = OpenAI()

tools = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current local date and time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

# 1. První dotaz na model
response = client.responses.create(
    model="gpt-5.4",
    input="Kolik je právě teď hodin?",
    tools=tools,
)

# 2. Najdeme požadavek na tool
tool_call = response.output[0]

print("Model wants to call:")
print(tool_call.name)

# 3. Skutečně spustíme naši Pythonovou funkci
if tool_call.name == "get_current_time":
    result = get_current_time()

print("Tool returned:")
print(result)

# 4. Výsledek toolu pošleme zpět modelu
response2 = client.responses.create(
    model="gpt-5.4",
    previous_response_id=response.id,
    input=[
        {
            "type": "function_call_output",
            "call_id": tool_call.call_id,
            "output": result,
        }
    ],
    tools=tools,
)

# 5. Finální odpověď
print("Final answer:")
print(response2.output_text)