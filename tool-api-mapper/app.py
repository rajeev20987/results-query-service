from fastapi import FastAPI
from ollama import chat
from mcp.client.sse import sse_client
from mcp import ClientSession
from ollama import Client
import os

app = FastAPI()

# MCP tool executor
async def execute_get_results(status=None, suite=None, name=None):
    args = {}
    if status:
        args["status"] = status
    if suite:
        args["suite"] = suite
    if name:
        args["name"] = name

    async with sse_client("http://mcp-tool:8080/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool("get_results", arguments=args)
            return str(result.content)

# tool registry
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_results",
            "description": "Fetch test execution results filtered by status, suite, test name, or limit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "description": "passed or failed"
                    },
                    "suite": {
                        "type": "string",
                        "description": "suite name such as smoke or regression"
                    },
                    "name": {
                        "type": "string",
                        "description": "specific test name"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "maximum number of results"
                    }
                }
            }
        }
    }
]

@app.get("/chat")
async def chat_endpoint(prompt: str):
    messages = [
        {
            "role": "system",
            "content": """
    You are an assistant for test execution reporting.

    Use the get_results tool whenever the user asks about:
    - failed tests
    - passed tests
    - smoke or regression suites
    - specific test names
    - latest test results

    Only ask follow-up questions if required information is missing.
    """
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    ollama_client = Client(host=os.getenv("OLLAMA_HOST"))
    while True:
        response = ollama_client.chat(
            model="qwen2.5:3b",
            messages=messages,
            tools=TOOLS
        )

        msg = response["message"]
        messages.append(msg)

        tool_calls = msg.get("tool_calls", [])

        if not tool_calls:
            return {"response": msg["content"]}

        for tc in tool_calls:
            fn = tc["function"]["name"]
            args = tc["function"]["arguments"]

            if fn == "get_results":
                tool_result = await execute_get_results(**args)

                messages.append({
                    "role": "tool",
                    "name": fn,
                    "content": str(tool_result)
                })