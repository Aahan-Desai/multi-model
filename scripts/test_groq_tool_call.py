from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "rag_search",
            "description": "Search documents",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string"
                    }
                },
                "required": ["question"]
            }
        }
    }
]

response = client.chat.completions.create(
    model="qwen/qwen3-32b",
    messages=[
    {
        "role": "system",
        "content": (
            "You are an AI router. "
            "You must use the provided tools whenever possible. "
            "Do not answer from your own knowledge."
        ),
    },
    {
        "role": "user",
        "content": "What is Section 1?"
    }
],
    tools=tools,
    tool_choice="required",
)

print(response)