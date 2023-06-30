from aiogram import types, Bot, Dispatcher, executor
from loguru import logger
from db import Database, create_db


logger.add("info.log", format="{time} {level} {message}", level="INFO", rotation="10 MB", compression="gz")
bot_token = 'none'
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
db = Database('users.sql')


@dp.message_handler(commands=['start'])
async def main(message: types.Message):
    create_db()

    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.first_name, message.from_user.last_name, message.from_user.id)

    await message.answer(f'Добро пожаловать {message.from_user.first_name} '
                                      f'{message.from_user.last_name}!\n'
                                      f'Сейчас тебя мы зарегестрируем.\n'
                                      f'Для ознакомление работы с чатом введите команду /help')


@dp.message_handler(commands=['ID'])
async def id_chat(message: types.Message):
    await message.answer(f'Чат ID: {message.chat.id}\n'
                         f'User ID: {message.from_user.id}')


@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message):
    await message.answer('Основные команды для работы с чат ботом:\n'
                                      '/help - Выводит основные команды \n'
                                      '/zadacha вывод времени на помощь')


@dp.message_handler(commands=['zadacha'])
async def zadacha(message: types.Message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Требуется помощь"))
    markup.add(types.KeyboardButton("Свободен"))
    await message.answer('Выберете один из вариантов', reply_markup=markup)


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    text_messag = message.text
    print(text_messag)
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список пользователей', callback_data='users'))
    await message.answer('Выводит список пользователей.', reply_markup=markup)


@dp.message_handler(content_types=['text'])
async def on_click(message: types.Message):
    if message.text == 'Требуется помощь':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Задача на 10 минут"), types.KeyboardButton("Задача на 15 минут"),
                   types.KeyboardButton("Задача на 30 минут"))
        markup.add(types.KeyboardButton("Задача на 45 минут"), types.KeyboardButton("Задача на 60 минут"),
                   types.KeyboardButton("Задача на 120 минут"))
        markup.add(types.KeyboardButton("Главное меню"))
        await message.answer('Выберете минимальное время для выполнение задачи', reply_markup=markup)
    elif message.text == 'Свободен':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Свободен на 60 минут"), types.KeyboardButton("Свободен на 120 минут"))
        markup.add(types.KeyboardButton("Свободен на 240 минут"), types.KeyboardButton("Свободен целый день"))
        markup.add(types.KeyboardButton("Главное меню"))
        await message.answer('Выберете один из вариантов', reply_markup=markup)
    elif message.text == 'Главное меню':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Требуется помощь"))
        markup.add(types.KeyboardButton("Свободен"))
        await message.answer('Выберете один из вариантов', reply_markup=markup)
    elif message.text == 'Свободен на 60 минут':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Могу помочь на 60 минут @{message.from_user.username}.'
                    logger.info(f"ID пользователя: {user_id[0]}")
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')
    elif message.text == 'Свободен на 120 минут':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Могу помочь на 120 минут @{message.from_user.username}.'
                    logger.info(f"ID пользователя: {user_id[0]}")
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')
    elif message.text == 'Свободен на 240 минут':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Могу помочь на 240 минут @{message.from_user.username}.'
                    logger.info(f"ID пользователя: {user_id[0]}")
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')
    elif message.text == 'Свободен целый день':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Свободен на целый день @{message.from_user.username}.'
                    logger.info(f"ID пользователя: {user_id[0]}")
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')
    elif message.text == 'Задача на 10 минут':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Требуется помощь на 10 минут @{message.from_user.username}.'
                    logger.info(f"ID пользователя: {user_id[0]}")
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')
    elif message.text == 'Задача на 15 минут':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Требуется помощь на 15 минут @{message.from_user.username}.'
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')
    elif message.text == 'Задача на 30 минут':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Требуется помощь на 30 минут @{message.from_user.username}.'
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')
    elif message.text == 'Задача на 45 минут':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Требуется помощь на 45 минут @{message.from_user.username}.'
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')
    elif message.text == 'Задача на 60 минут':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Требуется помощь на 60 минут @{message.from_user.username}.'
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')
    elif message.text == 'Задача на 120 минут':
        if message.chat.type == 'private':
            users = db.get_user()
            for user_id in users:
                try:
                    text = f'Требуется помощь на 120 минут @{message.from_user.username}.'
                    await bot.send_message(user_id[0], text)
                    if int(user_id[1]) != 1:
                        db.set_active(user_id[0], 1)
                except:
                    db.set_active(user_id[0], 0)
            await message.answer('Сообщение успешно отправлено')


@dp.callback_query_handler()
async def callback(call):
    await call.message.answer(db.list_user())
    await call.message.answer('в ведите Чат ID для удаления')


def start_bot():
    executor.start_polling(dp)


if __name__ == '__main__':
    start_bot()

