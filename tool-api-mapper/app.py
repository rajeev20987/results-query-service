from mcp.client.sse import sse_client
from mcp import ClientSession
from fastapi import FastAPI

app = FastAPI()

async def get_results_tool_call():
    async with sse_client("http://mcp-tool:8080/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()

            result = await session.call_tool(
                "get_results",
                arguments={"status": "failed"}
            )

            return result.content  # important fix


@app.get("/chat")
async def chat():
    return await get_results_tool_call()