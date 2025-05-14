import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN") or '7561017077:AAF0_aBLpMCQuX0wjDVgYNKH4-COxspmwQE'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Список нежелательных слов (вынесен в константу)
BAD_WORDS = {'плохое', 'слово', 'мат'}

# Хэндлеры команд
@dp.message(Command("start"))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')

@dp.message(Command("help"))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь и в ответ я пришлю тебе твое сообщение')

# Обработка фото (исправленная регистрация)
@dp.message(F.content_type == ContentType.PHOTO)
async def send_photo_echo(message: Message):
    await message.reply_photo(message.photo[-1].file_id)

# Команда /caps (исправленная версия)
@dp.message(Command("caps"))
async def cmd_caps(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Введите текст после команды, например: /caps привет")
        return
    await message.reply(args[1].upper())

# Команда /reverse (исправленная версия)
@dp.message(Command("reverse"))
async def cmd_reverse(message: types.Message):
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Введите текст после команды, например: /reverse привет")
        return
    await message.reply(args[1][::-1])

# Фильтр нежелательных слов (исправленный)
@dp.message(F.text.casefold().contains(BAD_WORDS))
async def bad_words_filter(message: types.Message):
    await message.reply("⚠️ Сообщение содержит недопустимые слова!")
    await message.delete()

# Фильтр цифр (исправленный)
@dp.message(F.text.regexp(r'\d'))
async def digits_filter(message: types.Message):
    digits = re.findall(r'\d', message.text)
    await message.reply(f"🔢 В вашем сообщении найдены цифры: {', '.join(digits)}")

# Эхо-обработчик (должен быть последним!)
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)

if __name__ == '__main__':
    dp.run_polling(bot)