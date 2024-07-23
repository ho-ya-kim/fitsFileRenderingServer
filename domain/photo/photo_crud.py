from models import Photo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from domain.photo.photo_schema import Description, PhotoCreate
from datetime import datetime
from sqlalchemy import and_


async def get_photo_list(db: AsyncSession, skip: int = 0, limit: int = 10, keyword: str = ''):
    if keyword:
        search = '%%{}%%'.format(keyword)
        query = select(Photo).select_from(Photo).filter(
            Photo.name.ilike(search) |
            Photo.description.ilike(search) |
            Photo.headers.ilike(search)
        )
    else:
        query = select(Photo)

    question_list = await db.execute(query)
    total = len(question_list.scalars().all())
    question_list = await db.execute(query.offset(skip).limit(limit))

    return total, question_list.scalars().all()


async def get_photo(db: AsyncSession, photo_id: int):
    photo = await db.get(Photo, photo_id)
    print(photo)
    return photo


async def update_description(db: AsyncSession, photo_id: int, description: Description):
    try:
        question = await db.get(Photo, photo_id)
        question.description = description.content
        await db.commit()
        return 1
    except:
        return 0


async def create_photo(db: AsyncSession, photo_create: PhotoCreate):
    db_photo = Photo(name=photo_create.name,
                     imagePath=photo_create.imagePath,
                     headers=photo_create.headers,
                     create_date=datetime.now())
    db.add(db_photo)
    await db.commit()
