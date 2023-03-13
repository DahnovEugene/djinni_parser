from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hlink
from aiogram.dispatcher.filters import Text
import os
from pars import *
import json


bot = Bot(os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
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
    writer_file('1y')

    with open('some_json.json') as f:
        data = json.load(f)

    for item in data:
        requirements = ''
        for el in item.get('requirements'):
            for i in el:
                requirements = requirements + i + '\n'
        card = f"{hlink(item.get('title'), item.get('link'))}\n" \
            f"{hbold(requirements)}"
        await message.answer(card)


def main():
    print('Bot started!')
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
