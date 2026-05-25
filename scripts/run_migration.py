import asyncio
import asyncpg
import sys
from pathlib import Path
from app.core.config import settings

DB_URLS = {
    "batches": settings.batches_db_url,
    "finance": settings.finance_db_url,
    "health": settings.health_db_url,
    "auth": settings.auth_db_url,
}

async def run_migration(module: str, migration_id: str):
    files = list(Path("migrations").glob(f"{module}/{migration_id}*.sql"))

    if not files:
        print(f"No migration file found for {module}/{migration_id}")
        sys.exit(1)

    sql = files[0].read_text()
    conn = await asyncpg.connect(DB_URLS[module])
    try:
        await conn.execute(sql)
        print(f"Migration {files[0].name} applied successfully")
    finally:
        await conn.close()

if __name__ == "__main__":
    module, migration_id = sys.argv[1], sys.argv[2]
    asyncio.run(run_migration(module, migration_id))
