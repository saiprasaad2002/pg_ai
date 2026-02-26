from src.mcp_server.server import PgMCP
import asyncio
from fastmcp.server.lifespan import lifespan
from src.connectors.pg_connector import PGConnector
from src.loaders.env_loader import get_mcp_settings
from src.logger.mcp_logger import get_mcp_logger

settings = get_mcp_settings()
logger = get_mcp_logger()

@lifespan
async def mcp_lifespan(server):
    try:
        conn = PGConnector(
            db_user=settings.db_user,
            db_host=settings.db_host,
            db_port=settings.db_port,
            db_pass=settings.db_pass,
            db_name=settings.db_name
        )
        database = await conn.connect()
        if database:
            logger.info(f"Connected with Database @ {settings.db_host}:{settings.db_port}")
            yield {"pg_connection": database, "logger": logger}
        else:
            logger.warning(f"No connection established @ {settings.db_host}:{settings.db_port}")
            raise Exception("MCP Server cannot be established without a database connection")
    finally:
        await conn.disconnect()
        logger.info(f"Database connection closed with {settings.db_host}:{settings.db_port}")


async def main():
    server_config = PgMCP(
        lifespan=mcp_lifespan, 
        server_name="pg_ai",
        instructions="MCP Server to handle database operations"
    )
    mcp_server = server_config.get_mcp_server()
    await mcp_server.run_async(
        transport=settings.mcp_server_transport,
        host=settings.mcp_server_host,
        port=settings.mcp_server_port
    )

if __name__ == "__main__":
    asyncio.run(main())

