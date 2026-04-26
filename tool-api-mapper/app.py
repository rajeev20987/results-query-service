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
            "description": "Fetch test execution results",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {"type": "string"},
                    "suite": {"type": "string"},
                    "name": {"type": "string"}
                }
            }
        }
    }
]

@app.get("/chat")
async def chat_endpoint(prompt: str):
    messages = [{"role": "user", "content": prompt}]
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
                    "tool_name": fn,
                    "content": tool_result
                })