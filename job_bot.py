from aiogram import Bot, Dispatcher, executor, types
import os


bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['no_exp', '1y', '2y', '3y', '4y', '5y', '/start']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Hello!', reply_markup=keyboard)


@dp.message_handler(text=['no_exp', '1y', '2y', '3y', '4y', '5y'])
async def get_result():
    pass


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
