import asyncpg
import asyncio

PG_HOST = "postgres"
PG_DB = "eventdb"
PG_USER = "event_user"
PG_PASSWORD = "event_pass"
PG_PORT = 5432

_db_pool = None

async def get_pool():
    global _db_pool
    if _db_pool is None:
        _db_pool = await asyncpg.create_pool(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASSWORD,
            database=PG_DB,
            min_size=1,
            max_size=10
        )
    return _db_pool

async def fetch_all(query, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetch(query, *args)

async def fetch_one(query, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchrow(query, *args)

async def execute(query, *args):
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.execute(query, *args)
