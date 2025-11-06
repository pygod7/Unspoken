# test_vps_pg_remote.py
import asyncio
import asyncpg
from app.settings import Settings
config = Settings()

async def main():
    try:
        conn = await asyncpg.connect(config.DATABASE_URL)
        print("✅ VPS PostgreSQL is reachable remotely!")
        await conn.close()
    except Exception as e:
        print("❌ Remote connection failed:", e)

asyncio.run(main())
