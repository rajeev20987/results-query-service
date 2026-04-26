from mcp.server.fastmcp import FastMCP
import requests
from typing import Optional
import uvicorn

mcp = FastMCP("ResultsTools")

API_BASE_URL = "http://result-query-service:8000"

@mcp.tool()
def get_results(status: Optional[str] = None):
    params = {"status": status} if status else {}
    r = requests.get(f"{API_BASE_URL}/results", params=params)
    return r.json()

app = mcp.sse_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080, proxy_headers=True)