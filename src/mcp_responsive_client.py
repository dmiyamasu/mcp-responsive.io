#!/usr/bin/env python3
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import json
import os
import asyncio

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python3",  # Executable
    args=["mcp_responsive.py"],  # Optional command line arguments
    env={ "RESPONSIVE_API_TOKEN": os.environ.get('RESPONSIVE_API_TOKEN') }  # Optional environment variables
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            prompts = await session.list_prompts()
            print(f'prompts: {prompts}')

            # List available resources
            resources = await session.list_resources()
            print(f'resources: {resources}')

            # List available tools
            tools = await session.list_tools()
            print(f'tools: {tools}')

            # Call a tool
            result = await session.call_tool("search_content", arguments={"keyword": "conduct"})
            print('search results:', result)

if __name__ == "__main__":
    asyncio.run(run())