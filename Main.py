import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ContentType
from aiogram.filters import Command
from aiogram.types import Message
from dotenv import load_dotenv
import os
load_dotenv()
BOT_TOKEN = os.getenv("7561017077:AAF0_aBLpMCQuX0wjDVgYNKH4-COxspmwQE")

# Вместо BOT TOKEN HERE нужно вставить токен вашего бота, полученный у @BotFather
BOT_TOKEN = '7561017077:AAF0_aBLpMCQuX0wjDVgYNKH4-COxspmwQE'

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


# Этот хэндлер будет срабатывать на отправку боту фото
async def send_photo_echo(message: Message):
    print(message)
    await message.reply_photo(message.photo[0].file_id)
    dp.message.register(send_photo_echo, F.content_type == ContentType.PHOTO)


# Команда /caps
@dp.message(Command("caps"))
async def cmd_caps(message: types.Message, command: types.Command):
    if not command.args:
        await message.reply("Введите текст после команды, например: /caps привет")
        return
    await message.reply(command.args.upper())

# Команда /reverse
@dp.message(Command("reverse"))
async def cmd_reverse(message: types.Message, command: types.Command):
    if not command.args:
        await message.reply("Введите текст после команды, например: /reverse привет")
        return
    await message.reply(command.args[::-1])

# Фильтр для нежелательных слов
BAD_WORDS = {'плохое', 'слово', 'мат'}

@dp.message(F.text.lower().contains(BAD_WORDS))
async def bad_words_filter(message: types.Message):
    await message.reply("⚠️ Сообщение содержит недопустимые слова!", reply=False)
    await message.delete()

# Фильтр для сообщений с цифрами
@dp.message(F.text.regexp(r'\d').as_("has_digits"))
async def digits_filter(message: types.Message, has_digits: re.Match):
    await message.reply(f"🔢 В вашем сообщении найдены цифры: {has_digits.group()}")


# Фильтр для нежелательных слов
BAD_WORDS = {'плохое', 'слово', 'мат'}

@dp.message(F.text.lower().contains(BAD_WORDS))
async def bad_words_filter(message: types.Message):
    await message.reply("⚠️ Сообщение содержит недопустимые слова!", reply=False)
    await message.delete()

# Фильтр для сообщений с цифрами
@dp.message(F.text.regexp(r'\d').as_("has_digits"))
async def digits_filter(message: types.Message, has_digits: re.Match):
    await message.reply(f"🔢 В вашем сообщении найдены цифры: {has_digits.group()}")

if __name__ == '__main__':
    dp.run_polling(bot)