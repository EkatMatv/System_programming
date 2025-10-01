"""
Вам необходимо реализовать небольшой асинхронный API-сервис с использованием библиотеки aiohttp.
Сервис должен предоставлять следующие возможности:
Эндпоинт / (GET)
Возвращает приветственное сообщение в формате JSON, например:
{ "message": "Добро пожаловать в наш сервис!" }

Эндпоинт /items (GET)
Возвращает список всех элементов (данные можно хранить в обычном Python-списке в памяти).
Формат ответа:
{ "items": ["item1", "item2", "item3"] }

Эндпоинт /items (POST)
Принимает JSON с полем "name" и добавляет элемент в список.
Пример запроса:
{ "name": "новый_элемент" }

Пример ответа:
{ "message": "Элемент успешно добавлен" }

Эндпоинт /items/{id} (GET)
Возвращает элемент по индексу (например, /items/0 → item1).
Если элемент не найден, возвращает ошибку 404 и JSON с сообщением.
Эндпоинт /items/{id} (DELETE)
Удаляет элемент по индексу.
Возвращает сообщение об успешном удалении или ошибку, если индекс не существует.

Рекомендации по реализации:
Запуск aiohttp-сервера
Подумайте, как мы запускали сервер на aiohttp на лекции.
Вспомните, что используется web.Application() и функция web.run_app(...).

Маршруты
Маршруты (эндпоинты) в aiohttp добавляются через app.router.add_get(...), add_post(...), add_delete(...).
Вспомните, что внутри обработчика запроса мы используем async def.

Возврат JSON-ответа
aiohttp имеет специальную функцию web.json_response(...).
Подумайте, как можно вернуть словарь Python в виде JSON.

Хранение данных
Данные можно хранить в обычном Python-списке, например items = [].
Для простоты храните его прямо в глобальной области видимости.

POST-запрос (добавление элемента)
Для извлечения данных из POST-запроса используйте await request.json().
Подумайте, как из полученного словаря достать поле "name".

GET по индексу (/items/{id})
Чтобы получить индекс из URL, используйте request.match_info["id"].
Не забудьте преобразовать его в int.

Обработка ошибок (404)
Если индекс выходит за пределы списка, верните web.json_response({"error": "Элемент не найден"}, status=404).

DELETE-запрос
Используйте del items[index] для удаления.
Не забудьте обработать ситуацию, если индекс неверный.
"""
from aiohttp import web

items = ["item1", "item2", "item3"]

async def hello(request):
    return web.json_response({"message": "Добро пожаловать в наш сервис!"})

async def get_items(request):
    return web.json_response({"items": items})

async def post_items(request):
    data = await request.json()
    items.append(data["name"])
    return web.json_response({"message": "Элемент успешно добавлен"})

async def get_item(request):
    item_id = int(request.match_info["id"])
    if item_id >= len(items):
        return web.json_response({"error": "Элемент не найден"}, status=404)
    return web.json_response({"item": items[item_id]})

async def delete_item(request):
    item_id = int(request.match_info["id"])
    if item_id >= len(items):
        return web.json_response({"error": "Элемент не найден"}, status=404)
    items.pop(item_id)
    return web.json_response({"message": "Элемент успешно удален"})

app = web.Application()
app.router.add_get('/', hello)
app.router.add_get('/items', get_items)
app.router.add_post('/items', post_items)
app.router.add_get('/items/{id}', get_item)
app.router.add_delete('/items/{id}', delete_item)

if __name__ == '__main__':
    web.run_app(app)