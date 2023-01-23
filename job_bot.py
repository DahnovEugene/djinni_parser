from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
import os
from pars import get_data
import json


bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['no_exp', '1y', '2y', '3y', '4y', '5y', '/start']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('choose something', reply_markup=keyboard)


@dp.message_handler(Text(equals='1y'))
async def get_result(message: types.Message):
    await message.answer('Wait a minute...')

    get_data('1y')
    with open('some_json.json') as f:
        data = json.load(f)

    # data = get_data('1y')

    for el in data:
        await message.answer(el['link'])


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
