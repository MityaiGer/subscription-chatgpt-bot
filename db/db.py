import asyncpg
from config import DB


class AsyncpgConn:
    async def __aenter__(self):
        self.conn = await asyncpg.connect(**DB)
        return self.conn
    async def __aexit__(self, ex_type, ex_value, traceback):
        await self.conn.close()

class AsyncDB:
    async def execute_query(self, query, *args):
        async with AsyncpgConn() as conn:
            return await conn.fetch(query, *args)
