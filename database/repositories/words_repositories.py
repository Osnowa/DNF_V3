from database.models import DBWords
from database.db import AsyncSession
from sqlalchemy import select, delete

import logging

logger = logging.getLogger(__name__)


class Words_Repositories:
    '''Класс для работы с БД -> CRUD'''
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_word(self, word_get):
        '''Добавляем слово'''
        stmt = DBWords(word=word_get.word, word_translate=word_get.word_translate)
        self.session.add(stmt)
        await self.session.commit()
        await self.session.refresh(stmt)
        return stmt

    async def get_words(self):
        '''Получаем все слова'''
        stmt = select(DBWords) # сам запрос
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_word(self, word_id: int):
        '''Получаем слово'''
        stmt = select(DBWords).where(DBWords.id == word_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_word(self, word_id: int):
        '''Удаляем слово'''
        word = await self.get_word(word_id)
        if word:
            await self.session.delete(word)
            await self.session.commit()
            return True
        else:
            return False

    async def delete_all_words(self):
        """Удаляем все слова"""
        stmt = delete(DBWords)
        await self.session.execute(stmt)
        await self.session.commit()

    async def patch_word(self, word_id: int, word_get):
        '''Обновляем слово'''
        word = await self.get_word(word_id)
        if not word:
            return False
        for key,value in word_get.model_dump(exclude_unset=True).items(): # получаем только измененные поля
            setattr(word, key, value) # обновляем поля
        await self.session.commit()
        return word