from pydantic import BaseModel, Field
from typing import List, Callable, Any

class Content(BaseModel):
    content: str = Field(description="The returned skill file content")

class MCPTools(BaseModel):
    mcp_tools: List[Callable] = Field(description="List of MCP tools to be used to host the MCP server")

class DatabaseResult(BaseModel):
    sql_query: str = Field(description="The prepared sql query")
    sql_result: Any = Field(description="The result of sql execution wrapped as DataFrame")

