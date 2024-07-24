import json

from models import Photo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc
from sqlalchemy.future import select
from domain.photo.photo_schema import Description, PhotoCreate, Name
from datetime import datetime
from fastapi import UploadFile
import uuid
from aiofiles import open as aioopen
from fastapi.responses import FileResponse
from base64 import b64encode

from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm


async def get_photo_list(db: AsyncSession, skip: int = 0, limit: int = 10, keyword: str = ''):
    if keyword:
        search = '%%{}%%'.format(keyword)
        query = select(Photo).select_from(Photo).filter(
            Photo.name.ilike(search) |
            Photo.description.ilike(search) |
            Photo.headers.ilike(search)
        ).order_by(desc(Photo.create_date), desc(Photo.id))
    else:
        query = select(Photo).order_by(desc(Photo.create_date), desc(Photo.id))

    question_list = await db.execute(query.order_by(Photo.create_date))
    total = len(question_list.scalars().all())
    question_list = await db.execute(query.offset(skip).limit(limit))

    return total, question_list.scalars().all()


async def get_photo(db: AsyncSession, photo_id: int):
    photo = await db.get(Photo, photo_id)

    with fits.open(f".\images\{photo.imagePath}") as fits_file:
        image_data = fits_file[0].data
        plt.figure()
        plt.imshow(image_data, origin='lower', norm=LogNorm(), cmap='gist_grey')
        plt.axis('off')
        plt.savefig(".\log\image.jpg", bbox_inches='tight', pad_inches=0)

    async with aioopen(".\log\image.jpg", 'rb') as img:
        img_read = await img.read()
        val = b64encode(img_read)

    print(photo)
    return photo, val


async def update_description(db: AsyncSession, photo_id: int, description: Description):
    try:
        photo = await db.get(Photo, photo_id)
        photo.description = description.content
        await db.commit()
        return 1
    except:
        return 0


async def update_name(db: AsyncSession, photo_id: int, name: Name):
    try:
        photo = await db.get(Photo, photo_id)
        photo.name = name.content
        await db.commit()
        return 1
    except:
        return 0


async def create_photo(db: AsyncSession, photo_create: PhotoCreate):
    db_photo = Photo(name=photo_create.name,
                     imagePath=photo_create.imagePath,
                     headers=photo_create.headers,
                     description='no description',
                     create_date=datetime.now())
    db.add(db_photo)
    await db.commit()


async def upload_file(db: AsyncSession, file: UploadFile):
    print(file)
    upload_path = '.\images'
    contents = await file.read()
    filename = f"{str(uuid.uuid4())}.fits"
    filepath = f"{upload_path}\{filename}"
    async with aioopen(filepath, "wb") as fp:
        await fp.write(contents)

    with fits.open(filepath) as fits_file:
        async with aioopen('.\log\header.txt', 'w') as header_log:
            await header_log.write(repr(fits_file[0].header))

    with open('.\log\header.txt', 'r') as header_log:
        header = header_log.readlines()
    headers = {}
    for hdr in header:
        kwd = hdr.split('=')[0].strip()
        val = hdr.split('=')[1].split('/')[0].strip()
        com = hdr.split('=')[1].split('/')[1].strip()

        headers[kwd] = (val, com)

    print(headers)

    name = 'new file _' + datetime.now().strftime("%Y.%m.%d. %H:%M:%S")
    await create_photo(db=db,
                       photo_create=PhotoCreate(name=name,
                                                imagePath=filename,
                                                headers=json.dumps(headers)))

    return filepath


async def download_file(db: AsyncSession, photo_id: int):
    photo = await db.get(Photo, photo_id)
    print(photo.imagePath)
    async with aioopen(f".\images\{photo.imagePath}", 'r') as f:
        print(f)
    return FileResponse(f".\images\{photo.imagePath}", filename=photo.name + '.fits')
