from typing import Annotated
from environs import Env
from fastapi import Depends
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

import logging


logger = logging.getLogger(__name__)

env = Env()
env.read_env()

# Наша БД в контейнере
DATABASE_URL = env.str('DB_URL') # путь к базе данных

engine = create_async_engine(DATABASE_URL, 
    pool_size = 5,
    max_overflow = 10,
    pool_pre_ping = True
    ) # создаем движок и настраиваем пул соединений

SessionFactory = async_sessionmaker(engine, expire_on_commit=False) # создаем генератор сессий

class Base(DeclarativeBase):
    '''Класс для всех моделей (таблиц)'''
    pass


### === Убираем создание таблиц, так как этим займется alembic === ###


# async def create_tables():
#     '''Создание таблиц, не понадобится при alembic'''
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all) 

async def disponse_engine():
    '''Закрываем все соединения при остановке приложения'''
    logger.info('Закрытие движка БД')
    await engine.dispose()


async def get_session():
    '''Открываем сессию и отдаем ее'''
    async with SessionFactory() as session:
        logger.info('Открытие сессии')
        yield session # выступает как генератор, работает до тех пор, пока открыта функция, куда передается сессия

SessionDep = Annotated[AsyncSession, Depends(get_session)] # теперь в каждом эндпоинте, при параметре SessionDep, 
# будет вызываться функция get_session и ее значение передается в эндпоинт