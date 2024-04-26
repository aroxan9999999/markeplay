import os
from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from database import Chat, session

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def send_excel(chat_id, path):
    file = FSInputFile(path)
    await bot.send_document(chat_id, file)


@dp.message(CommandStart())
async def handle_start(message: Message):
    chat_id = message.chat.id
    existing_chat = session.query(Chat).filter(Chat.chat_id == chat_id).first()
    if existing_chat is None:
        chat = Chat(chat_id=chat_id)
        session.add(chat)
        session.commit()

    await send_excel(chat_id, 'orders.xlsx')
    await send_excel(chat_id, 'sales.xlsx')


async def marketplay_bot() -> None:
    await dp.start_polling(bot)
