from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Photo(Base):
    __tablename__ = 'photo'

    id = Column(Integer, primary_key=True)  # 각 사진의 고유 ID
    name = Column(String(100), nullable=False)  # 웹에서 표기될 이름
    imagePath = Column(Text, nullable=False)  # Local에 있는 사진의 path
    description = Column(Text, nullable=False)  # 사진에 대한 상세설명
    headers = Column(Text, nullable=False)  # Fits Headers
    create_date = Column(DateTime, nullable=False)  # 사진 업로드 날짜, 촬영 시간과 다름
