from sqlalchemy.orm import Mapped, mapped_column

from database.db import Base

class DBWords(Base):
    '''Наша таблица'''
    __tablename__ = 'words'
    id : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    word : Mapped[str]
    word_translate : Mapped[str]