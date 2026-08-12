from fastapi import APIRouter, HTTPException, status
from database.db import SessionDep
from database.repositories.words_repositories import Words_Repositories
from shemas import WordAdd, WordGet, Update_Word
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/words",
    tags=["слова"]
)


@router.get("/", response_model=list[WordGet])
async def get_words(session: SessionDep):
    '''Получаем все слова'''
    logger.info('Заходим в ручку получения слов')
    words = await Words_Repositories(session).get_words()
    return words

@router.get("/{word_id}", response_model=WordGet)
async def get_word(word_id: int, session: SessionDep):
    '''Получаем 1 слово'''
    logger.info('Заходим в ручку получения слова')
    word = await Words_Repositories(session).get_word(word_id)
    if word:
        return word
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Слово не найдено")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=WordGet)
async def add_word(word_get: WordAdd, session: SessionDep):
    '''Добавляем слово'''
    logger.info('Заходим в ручку добавления слова')
    word = await Words_Repositories(session).add_word(word_get)
    return word

@router.patch("/{word_id}", response_model=WordGet)
async def update_word(word_id: int, word_get: Update_Word, session: SessionDep):
    """Обновляем слово"""
    logger.info('Заходим в ручку обновления слова')
    word = await Words_Repositories(session).patch_word(word_id, word_get)
    if word:
        return word
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Слово не найдено")


@router.delete("/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_word(word_id: int, session: SessionDep):
    '''Удаляем слово'''
    logger.info('Заходим в ручку удаления слова')
    result = await Words_Repositories(session).delete_word(word_id)
    if result:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Слово не найдено")

@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_all_words(session: SessionDep):
    '''Удаляем все слова'''
    logger.info('Заходим в ручку удаления всех слов')
    await Words_Repositories(session).delete_all_words()
    return None


