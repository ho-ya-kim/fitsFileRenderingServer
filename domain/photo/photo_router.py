from fastapi import APIRouter, Depends, status, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_db
from domain.photo import photo_schema, photo_crud

router = APIRouter(
    prefix="/api/photo",
)


@router.get("/list", response_model=photo_schema.PhotoList)
async def photo_list(db: AsyncSession = Depends(get_async_db), page: int = 0, size: int = 10, keyword: str = ''):
    total, _photo_list = await photo_crud.get_photo_list(db, skip=page * size, limit=size, keyword=keyword)
    print(_photo_list)
    return {'total': total, 'photo_list': _photo_list}


@router.get("/detail/{photo_id}", response_model=photo_schema.PhotoPreview)
async def photo_detail(photo_id: int, db: AsyncSession = Depends(get_async_db)):
    photo, val = await photo_crud.get_photo(db, photo_id=photo_id)
    return {'photo': photo, 'image': val}


@router.post("/description/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_description(photo_id: int, description: photo_schema.Description, db: AsyncSession = Depends(get_async_db)):
    print(description.content)
    await photo_crud.update_description(db=db, photo_id=photo_id, description=description)


@router.post("/rename/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_name(photo_id: int, name: photo_schema.Name, db: AsyncSession = Depends(get_async_db)):
    print(name.content)
    await photo_crud.update_name(db=db, photo_id=photo_id, name=name)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def create_photo(photo_create: photo_schema.PhotoCreate, db: AsyncSession = Depends(get_async_db)):
    await photo_crud.create_photo(db=db, photo_create=photo_create)


@router.post("/upload", status_code=status.HTTP_204_NO_CONTENT)
async def upload_photo(file: UploadFile, db: AsyncSession = Depends(get_async_db)):
    print(file)
    await photo_crud.upload_file(db=db, file=file)


@router.get("/download/{photo_id}")
async def download_photo(photo_id: int, db: AsyncSession = Depends(get_async_db)):
    return await photo_crud.download_file(db=db, photo_id=photo_id)
