from fastapi import APIRouter, Depends, status
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


@router.get("/detail/{photo_id}", response_model=photo_schema.Photo)
async def photo_detail(photo_id: int, db: AsyncSession = Depends(get_async_db)):
    photo = await photo_crud.get_photo(db, photo_id=photo_id)
    return photo


@router.post("/description/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_description(photo_id: int, description: photo_schema.Description, db: AsyncSession = Depends(get_async_db)):
    print(description.content)
    await photo_crud.update_description(db=db, photo_id=photo_id, description=description)


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
async def create_photo(photo_create: photo_schema.PhotoCreate, db: AsyncSession = Depends(get_async_db)):
    await photo_crud.create_photo(db=db, photo_create=photo_create)
