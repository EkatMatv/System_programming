"""
Настроить пул соединений к базе данных при помощи asyncpg в фикстуре.
Создать таблицу users для хранения пользователей.
Написать тесты с использованием pytest-asyncio для проверки корректности работы с базой данных.
Перед каждым тестом очищать таблицу.
Проверить как корректные операции, так и ошибки.

1. Создание таблицы пользователей:
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

2. Очистка таблицы:
TRUNCATE users;

3. Вставка нового пользователя:
INSERT INTO users (name) VALUES ($1);

4. Выбор всех пользователей:
SELECT * FROM users;

5. Поиск пользователя по имени:
SELECT id FROM users WHERE name = $1;

Создайте тестовый файл test_app.py.
Определите асинхронную фикстуру pool при помощи декоратора
Фикстура должна:
Создавать пул соединений с базой данных.
Выполнять SQL для создания таблицы, если она ещё не создана.
Очищать таблицу перед каждым тестом при помощи TRUNCATE.
Закрывать пул соединений после выполнения всех тестов.

Реализуйте тесты:
Тест 1. Добавление одного пользователя и проверка, что он появился в таблице.
Тест 2. Добавление нескольких пользователей и проверка количества строк.
Тест 3. Попытка добавить пользователя с пустым именем.
"""
import pytest
import asyncpg
import pytest_asyncio


@pytest_asyncio.fixture
async def pool():
    """Фикстура для создания пула соединений с базой данных"""

    pool = await asyncpg.create_pool(
        "postgresql://postgres:postgres@localhost/test_db",
        min_size=1,
        max_size=10
    )

    # Создаем таблицу если она не существует
    async with pool.acquire() as conn:
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL
            )
        ''')

    yield pool

    await pool.close()


@pytest_asyncio.fixture
async def clean_table(pool):
    """Фикстура для очистки таблицы перед каждым тестом"""
    async with pool.acquire() as conn:
        await conn.execute('TRUNCATE users')


@pytest.mark.asyncio
async def test_add_single_user(pool, clean_table):
    """Тест 1: Добавление одного пользователя и проверка его наличия"""
    async with pool.acquire() as conn:
        await conn.execute('INSERT INTO users (name) VALUES ($1)', 'John Doe')

    async with pool.acquire() as conn:
        users = await conn.fetch('SELECT * FROM users')

    assert len(users) == 1
    assert users[0]['name'] == 'John Doe'


@pytest.mark.asyncio
async def test_add_multiple_users(pool, clean_table):
    """Тест 2: Добавление нескольких пользователей и проверка количества"""
    users_data = ['Alice', 'Bob', 'Charlie']

    async with pool.acquire() as conn:
        for name in users_data:
            await conn.execute('INSERT INTO users (name) VALUES ($1)', name)

    async with pool.acquire() as conn:
        users = await conn.fetch('SELECT * FROM users')

    assert len(users) == len(users_data)

    user_names = [user['name'] for user in users]
    assert set(user_names) == set(users_data)


@pytest.mark.asyncio
async def test_add_user_with_empty_name(pool, clean_table):
    """Тест 3: Попытка добавить пользователя с пустым именем"""
    async with pool.acquire() as conn:
       with pytest.raises(asyncpg.exceptions.NotNullViolationError):
            await conn.execute('INSERT INTO users (name) VALUES ($1)', '')


@pytest.mark.asyncio
async def test_find_user_by_name(pool, clean_table):
    """Дополнительный тест: Поиск пользователя по имени"""

    async with pool.acquire() as conn:
        await conn.execute('INSERT INTO users (name) VALUES ($1)', 'Test User')
        await conn.execute('INSERT INTO users (name) VALUES ($1)', 'Another User')

    async with pool.acquire() as conn:
        user_id = await conn.fetchval(
            'SELECT id FROM users WHERE name = $1',
            'Test User'
        )

    assert user_id is not None
    assert isinstance(user_id, int)


@pytest.mark.asyncio
async def test_user_not_found(pool, clean_table):
    """Дополнительный тест: Поиск несуществующего пользователя"""
    async with pool.acquire() as conn:
        user_id = await conn.fetchval(
            'SELECT id FROM users WHERE name = $1',
            'Non Existent User'
        )

    assert user_id is None


@pytest.mark.asyncio
async def test_serial_auto_increment(pool, clean_table):
    """Дополнительный тест: Проверка автоинкремента ID"""
    async with pool.acquire() as conn:

        await conn.execute('INSERT INTO users (name) VALUES ($1)', 'First')
        await conn.execute('INSERT INTO users (name) VALUES ($1)', 'Second')

        users = await conn.fetch('SELECT * FROM users ORDER BY id')

    assert len(users) == 2
    assert users[0]['id'] == 1
    assert users[1]['id'] == 2
    assert users[0]['name'] == 'First'
    assert users[1]['name'] == 'Second'