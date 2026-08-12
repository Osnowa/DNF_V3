from pydantic import BaseModel, ConfigDict

class BaseWord(BaseModel):
    word: str
    word_translate: str

class WordAdd(BaseWord):
    '''Схема для получения от пользователя'''
    pass

class WordGet(BaseWord):
    '''То что отдаем пользователю'''
    id: int
    model_config = ConfigDict(from_attributes=True) # теперь мы сможем преобразовать sqlAlchemy в pydantic

class Update_Word(BaseModel):
    word: str | None = None
    word_translate: str | None = None
    model_config = ConfigDict(from_attributes=True)
