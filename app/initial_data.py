import asyncio

from db.init_db import init_db
from db.session import async_session


async def main() -> None:
    async with async_session() as session:
        await init_db(session)

if __name__ == "__main__":
    asyncio.run(main())
