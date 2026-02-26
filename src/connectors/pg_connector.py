# from sqlalchemy.ext.declarative import declarative_base
from databases import Database

class PGConnector:
    def __init__(self, db_user: str, db_pass: str, db_host: str, db_port: str, db_name: str):
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.DB_URL = f"postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    async def connect(self):
        try:
            self.database = Database(self.DB_URL)
            await self.database.connect()
            return self.database
        except Exception:
            raise
    
    async def disconnect(self):
        await self.database.disconnect()