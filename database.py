import sqlite3 as sq


async def db_start():
    global db, cur

    db = sq.connect('moneymanage.db')
    cur = db.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS money (
    user_id TEXT,
    cash INTEGER DEFAULT 0)
    ''')

    db.commit()  # функция создания таблицы в БД


async def add_cash(user_id, message_text):
    cur.execute('INSERT INTO money VALUES(?, ?)', (user_id, message_text))

async def load_cash(user_id):
    cash = cur.execute('SELECT cash FROM money WHERE user_id = ?', (user_id,)).fetchone()
    db.commit()
    return cash[0]  # функция вывода информации из БД


async def plus_cash(message_text, user_id):
    cur.execute('UPDATE money SET cash = cash+?  WHERE user_id = ?', (message_text, user_id))
    db.commit()   # функция добавления средств в БД


async def minus_cash(message_text, user_id):
    cur.execute('UPDATE money SET cash = cash-? WHERE user_id = ?', (message_text, user_id))
    db.commit()   # функция вычитания средств в БД
