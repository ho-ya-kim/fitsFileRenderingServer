import datetime

from pydantic import BaseModel


class Photo(BaseModel):
    id: int
    name: str
    imagePath: str
    description: str
    headers: str
    create_date: datetime.datetime


class Description(BaseModel):
    content: str

    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값으로 수정할 수 없습니다.')
        return v


class PhotoCreate(BaseModel):
    name: str
    imagePath: str
    headers: str

    @classmethod
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값으로 수정할 수 없습니다.')
        return v


class PhotoList(BaseModel):
    total: int
    photo_list: list[Photo] = []
