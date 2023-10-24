import asyncio

from app.db.init_db import init_db
from app.db.session import async_session


async def main() -> None:
    await init_db(async_session)


if __name__ == "__main__":
    asyncio.run(main())
