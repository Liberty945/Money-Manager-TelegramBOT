from config import TOKEN_API as bot_token
from aiogram import Bot, Dispatcher, types
from keyboards import get_keyboard, get_inline_keyboard
from database import add_cash, load_cash, plus_cash, minus_cash
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()


class Operations(StatesGroup):
    wait = State()
    select = State()
    plus = State()
    minus = State()


bot = Bot(bot_token)
dp = Dispatcher(bot, storage=storage)

counter_plus, counter_minus = 0, 0


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer('Введите сумму ваших средств', reply_markup=get_keyboard())
    await Operations.wait.set() #Хендлер команды start


@dp.message_handler(state=Operations.wait)
async def add_cash_db(message: types.Message):
    await add_cash(message.chat.id, message.text)
    await message.answer(f'Остаток средств: {await load_cash(message.chat.id)}')
    await Operations.select.set() #Хендлер создания записей в БД


@dp.message_handler(lambda message: message.text == 'Остаток средств', state=Operations.select)
async def cmd_check_money(message: types.Message):
    await message.delete()
    await message.answer(f'Остаток средств: {await load_cash(message.chat.id)}') #Хендлер вывода инфы из БД


@dp.message_handler(lambda message: message.text == 'Список операций', state=Operations.select)
async def cmd_change_money(message: types.Message):
    await message.delete()
    await message.answer('Какую операцию необходимо провести?', reply_markup=get_inline_keyboard()) #Хендлер вывода инлайн клавиатуры


@dp.callback_query_handler(state='*')
async def ikb_cb_check(callback: types.CallbackQuery):
    global counter_plus, counter_minus
    if counter_plus < 1 and counter_minus < 1:
        if callback.data == 'kb_plus':
            await callback.message.answer('Введите сумму поступления')
            counter_plus += 1
            await Operations.plus.set()
        else:
            await callback.message.answer('Введите сумму расходов')
            counter_minus += 1
            await Operations.minus.set()
    else:
        if counter_plus == 1:
            await callback.message.answer('Вы уже выбрали операцию (Поступления)')
        else:
            await callback.message.answer('Вы уже выбрали операцию (Расходы)')  #Обработчик callback query инлайн клавиатуры


@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) < 0, state='*')
async def check_isdigit(message: types.Message):
    await message.answer('Введите цифру (без знаков +, -)')  #Хендлер исключения not int


@dp.message_handler(state=Operations.plus)
async def plus_cash_db(message: types.Message, state: FSMContext):
    global counter_plus, counter_minus
    await plus_cash(message.text, message.chat.id)
    counter_plus, counter_minus = 0, 0
    await message.answer(f'Остаток средств: {await load_cash(message.chat.id)}')
    await Operations.select.set()  #Хендлер добавления средств в БД


@dp.message_handler(state=Operations.minus)
async def minus_cash_db(message: types.Message, state: FSMContext):
    global counter_plus, counter_minus
    await minus_cash(message.text, message.chat.id)
    counter_plus, counter_minus = 0, 0
    await message.answer(f'Остаток средств: {await load_cash(message.chat.id)}')
    await Operations.select.set()  #Хендлер убавления средств из БД
