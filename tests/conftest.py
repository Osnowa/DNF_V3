import pytest
import pytest_asyncio  
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from main import app
from database.db import get_session, Base
from database.models import DBWords

TEST_DATABASE_URL = "sqlite+aiosqlite:///test.db" # тестовая БД прямо в корне проекта, где запущен скрипт 

engine = create_async_engine(TEST_DATABASE_URL)
test_async_session = async_sessionmaker(engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setur_database():
    '''Создаем таблицы, передаем в приложение и удаляем после тестов'''
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield 

    # удаляем таблицы после тестов
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db():
    '''Обычная сессия — commit() внутри теста работает как обычно, никаких
    транзакционных костылей. Изоляция — очисткой таблиц после теста.'''
    async with test_async_session() as session:
        yield session

    async with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            await conn.execute(table.delete())


@pytest_asyncio.fixture
async def client(db):
    '''Создаем тестовое приложение, передаем в нее нашу сессию, заменяем зависимости'''
    async def override_get_db():
        yield db

    app.dependency_overrides[get_session] = override_get_db # подменяем Depends из нашего приложения

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as c :
        yield c

    app.dependency_overrides.clear()

### === Фикстра помошница, что бы не создавать запросы на наполнение БД === ###


@pytest_asyncio.fixture
async def test_words(db):
    '''Создаем тестовые слова внутри нашей БД'''
    words = [
        DBWords(word="apple", word_translate="яблоко"),
        DBWords(word="wear", word_translate="носить")
    ]
    db.add_all(words) # добавляем слова
    await db.commit()
    return words