import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import logging

# 配置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# 添加控制台处理程序
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

logger.info("lius_client start......")

server_params = {
        "command": "/home/lius/miniconda3/bin/fastmcp",
        "args": [
          "run",
          "/home/lius/sda1/tmp/github/duckduckgo-mcp-server/src/duckduckgo_mcp_server/server.py"
        ],
        "env": {
          
        }
}

# server_params = {
#         "command": "/home/lius/miniconda3/bin/fastmcp",
#         "args": [
#           "run",
#           "/home/lius/sda1/tmp/github/duckduckgo-mcp-server/src/echo_server/server.py"
#         ],
#         "env": {
          
#         }
# }


ssp: StdioServerParameters = StdioServerParameters(**server_params)

# Optional: create a sampling callback
async def handle_sampling_message(message: types.CreateMessageRequestParams) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )




async def main():
    async with stdio_client(ssp) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # List available prompts
            prompts = await session.list_prompts()
            logger.info(f"Available prompts: {prompts}")

            # Get a prompt
            #prompt = await session.get_prompt("example-prompt", arguments={"arg1": "value"})

            # List available resources
            resources = await session.list_resources()
            logger.info(f"Available resources: {resources}")
            
            # List available tools
            tools = await session.list_tools()
            logger.info(f"Available tools: {tools}")
            
            # Read a resource
            #content, mime_type = await session.read_resource("file://some/path")

            # Call a tool
            #result = await session.call_tool("fetch_content", arguments={"url": "https://huggingface.co/WizardLMTeam/WizardCoder-Python-34B-V1.0"})
            result = await session.call_tool("search", arguments={"query": "中国台湾"})
            #result = await session.call_tool("echo_tool", arguments={"message": "中国台湾"})
            logger.info(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())


# client 示例
# https://github.com/modelcontextprotocol/python-sdk/blob/main/examples/clients/simple-chatbot/mcp_simple_chatbot/main.py
