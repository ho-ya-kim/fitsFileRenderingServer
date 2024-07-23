from models import Photo
from datetime import datetime
from database import async_engine
from sqlalchemy.ext.asyncio import AsyncSession
import asyncio


asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
loop = asyncio.get_event_loop()


async def main(i):
    async with AsyncSession(bind=async_engine, expire_on_commit=False) as db:
        p = Photo(name=f'test name [{i}]', imagePath='test url', description='test description', headers='test info', create_date=datetime.now())
        db.add(p)

        # photo = await db.get(Photo, 1)
        # photo.headers = 'edited info'
        await db.commit()
    # print(photo.headers)

for i in range(300):
    loop.run_until_complete(main(i))
