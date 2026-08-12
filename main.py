from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from logging_setur import setur_logging
from database.db import disponse_engine
from router_words import router as router_words


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''Запускается один раз при старте и остановке приложения'''
    setur_logging() # вызываем настройки логов

    logger.info('Приложение запущено')
    yield
    await disponse_engine()


app = FastAPI(
    title='DNF_V3',
    description='Простое backand приложение для отработки навыков програмирования\n' \
    ' - Docker - PostgreSQL - Alembic - FastAPI - SQLAlchemy ',
    version='1.0.0',
    lifespan=lifespan
    )

app.include_router(router_words)