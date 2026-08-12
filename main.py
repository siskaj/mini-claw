import json

from openai import OpenAI
from tools import TOOLS

client = OpenAI()


tool_definitions = [
    {
        "type": "function",
        "name": "get_current_time",
        "description": "Get the current local date and time.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "type": "function",
        "name": "add_numbers",
        "description": "Add two numbers and return the result.",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number",
                },
                "b": {
                    "type": "number",
                    "description": "Second number",
                },
            },
            "required": ["a", "b"],
        },
    },
]


def run_agent(user_input: str) -> str:

    response = client.responses.create(
        model="gpt-5.4",
        input=user_input,
        tools=tool_definitions,
    )

    while True:

        tool_calls = [
            item
            for item in response.output
            if item.type == "function_call"
        ]

        # Model už nechce žádný tool → máme finální odpověď
        if not tool_calls:
            return response.output_text

        tool_outputs = []

        # Provedeme všechny tool calls
        for tool_call in tool_calls:

            tool_name = tool_call.name
            arguments = json.loads(tool_call.arguments)

            print()
            print(f"[tool] {tool_name}")
            print(f"[arguments] {arguments}")

            tool_function = TOOLS[tool_name]

            result = tool_function(**arguments)

            print(f"[result] {result}")

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": tool_call.call_id,
                    "output": str(result),
                }
            )

        # Výsledky všech tools vrátíme modelu
        response = client.responses.create(
            model="gpt-5.4",
            previous_response_id=response.id,
            input=tool_outputs,
            tools=tool_definitions,
        )


while True:

    user_input = input("\nYou > ")

    if user_input.lower() in {"exit", "quit"}:
        break

    answer = run_agent(user_input)

    print(f"\nAgent > {answer}")