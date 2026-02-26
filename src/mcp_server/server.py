from fastmcp import FastMCP
from src.mcp_tools.tools import get_mcp_tools
from fastmcp.server.lifespan import Lifespan

class PgMCP:
    def __init__(self,
                 lifespan: Lifespan, 
                 server_name: str | None = None, 
                 instructions: str | None = None,
                 version: str | None = None,
                 website_url: str | None = None,
                ):
        self.lifespan = lifespan
        self.server_name = server_name
        self.instructions = instructions
        self.version = version
        self.website_url = website_url
        tools = get_mcp_tools()
        self.mcp_tools = tools.mcp_tools

    def get_mcp_server(self):
        mcp_server = FastMCP(
            lifespan=self.lifespan,
            name=self.server_name,
            instructions=self.instructions,
            version=self.version,
            website_url=self.website_url,
            tools=self.mcp_tools
        )
        return mcp_server
