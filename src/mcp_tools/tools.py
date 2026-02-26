from pathlib import Path
from src.types.pg_ai_types import Content, DatabaseResult, MCPTools
from fastmcp import Context
from sqlalchemy import text
import polars as pl

async def read_business_logic():
    try:
        with open(Path("pg_skills")/"business-logic"/"SKILL.md", encoding="utf-8") as bl:
            content = bl.read()
        return Content(content=content)
    except Exception as e:
        raise e

async def load_skill(skill_name: str):
    """
    Load the respective skill to get the references for table schema, query instructions, etc.,
    """
    try:
        with open(Path("pg_skills")/skill_name/"SKILL.md", encoding="utf-8") as skill:
            content = skill.read()
        return Content(content=content)
    except Exception as e:
        raise e
    
async def execute_query(sql_query: str, ctx: Context):
    """
    Tool to execute the prepared sql query in the Postgres database
    """
    database = ctx.lifespan_context.get("pg_connection")
    try:
        if database:
            result = await database.fetch_all(text(sql_query))
            dataframe = pl.DataFrame(result)
            return DatabaseResult(sql_query=sql_query,sql_result=dataframe)
        return Content(content="No database connection acquired")
    except Exception as e:
        raise e


def get_mcp_tools():
    return MCPTools(
        mcp_tools=[read_business_logic, load_skill, execute_query]
    )