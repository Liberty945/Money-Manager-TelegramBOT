from database import db_start


async def on_shutdown(_):
    print('Бот остановлен')  # функция отрабатывает после остановки бота


async def db_startup(_):
    await db_start()  # функция создания БД
