# MCP-Based Test Results Agent

This repository demonstrates a containerized AI agent system that can fetch and summarize test execution results using:

* an LLM (via Ollama)
* an MCP (Model Context Protocol) tool server
* a FastAPI orchestrator
* a backend results service + database

## Architecture Overview

```text
User → Orchestrator (Agent) → LLM → MCP Tool → Result Service → DB
                                   ↑
                             Tool Response
```

## Components

| Service                        | Description                           |
| ------------------------------ | ------------------------------------- |
| model-runner                   | Runs the LLM (Ollama)                 |
| tool-api-mapper (orchestrator) | Agent layer (LLM + tool-calling loop) |
| mcp-tool                       | MCP server exposing tools             |
| result-query-service           | Backend API for fetching test results |
| db                             | PostgreSQL database                   |

## Features

* Natural language queries like:

  * show failed tests
  * show passed smoke tests
  * did login_test fail?
* Automatic tool selection via LLM
* Structured tool calling using MCP
* Dockerized microservices
* Extensible architecture for adding more tools

## Setup

### Start services

```bash
docker compose up --build
```

### Pull model

```bash
docker exec -it model-runner ollama pull qwen2.5:3b
```
* for now, start.sh pulls a qwen2.5:3b upon container spin-up.

## Usage

```bash
curl "http://localhost:<port>/chat?prompt=show failed smoke tests"
```

## Example Flow

1. User prompt:

   ```text
   show failed smoke tests
   ```

2. LLM emits tool call:

   ```json
   {
     "tool_calls": [
       {
         "function": {
           "name": "get_results",
           "arguments": {
             "status": "failed",
             "suite": "smoke"
           }
         }
       }
     ]
   }
   ```

3. MCP tool queries backend:

   ```text
   GET /results?status=failed&suite=smoke
   ```

4. LLM summarizes the response.

## Extending the System

Future tools:

* get_test_logs
* rerun_test
* get_build_status

## Notes

* Use same MCP SDK version across services.
* Stronger models improve tool-calling reliability.
