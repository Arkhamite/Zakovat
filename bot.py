import asyncio
import logging
import sys
from Zakovat import Savollar

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
import random

TOKEN = "Your TOKEN"


dp = Dispatcher()



@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Salom, {html.bold(message.from_user.full_name)}!\n\nO'yinni boshlash uchun /savol buyrug'ini bosing")


hammasi = {}
index1 = 0
javob1 = {}
pids = {}
@dp.message(Command("savol"))
async def savol(message: Message) -> None:
    if message.chat.id in pids and len(message.text) == 6:
        index = random.randint(0, 35)
        index1 = index
        savollar, javoblar = hammasi['data']
        try:
            javob1[message.chat.id] = javoblar[index]
            savol_index = f"{index+1}-Savol\n\n{savollar[index]}"
            await message.answer(savol_index)
        except:
            await message.answer("Bunday ID mavjud emas")
    elif len(message.text) > 6:
        pid = message.text[7:len(message.text)]
        pids[message.chat.id] = pid
        hammasi['data'] = Savollar(pids[message.chat.id])
    else:
        await message.answer("Paket IDini kiriting!")
        

@dp.message(Command("javob"))
async def taslim(message: Message) -> None:
    await message.answer(javob1[message.chat.id])

tries_dict = {}
@dp.message(lambda message: message.reply_to_message)
async def javob(message: Message):

    user_id = message.chat.id

    if user_id not in tries_dict:
        tries_dict[user_id] = 3

    if javob1[user_id].lower() == message.text.lower():
        await message.answer("To'g'ri javob")
        tries_dict[user_id] = 3 
    else:
        tries_dict[user_id] -= 1

        if tries_dict[user_id] > 0:
            await message.answer("Xato")
            await message.answer(f"Sizda {tries_dict[user_id]} ta urinish qoldi!")
        else:
            await message.answer(f"To'g'ri javob: {javob1[user_id]} edi")
            tries_dict[user_id] = 3
            

async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())