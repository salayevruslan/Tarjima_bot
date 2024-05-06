import asyncio, logging, os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters.command import CommandStart
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.context import FSMContext
from googletrans import Translator
from config import TOKEN, speech 
from buttons import menu, voice
from states import Translate_bot


logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
t = Translator()

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    fullname = message.from_user.full_name
    await message.answer(f"welcome, {fullname}", reply_markup=menu)
    await state.set_state(Translate_bot.lang)


@dp.message(F.text, Translate_bot.lang)
async def echo_handler(message: Message, state: FSMContext):
    language = message.text
    await state.update_data(
        {"lang": language} 
    )
    await state.set_state(Translate_bot.trans)
    await message.answer("So`zni kiriting: ")


@dp.message(Translate_bot.trans)
async def trans_handler(message: Message, state: FSMContext):
    txt = message.text
    d = await state.get_data()
    tarjima = d.get("lang")
    if tarjima == '🇺🇿 Uz -> 🇷🇺 Ru':
        xabar = t.translate(text=txt, dest='ru').text
        await message.answer(xabar, reply_markup=voice)
        speech(mytext=xabar, lan='ru')
    elif tarjima == '🇷🇺 Ru -> 🇺🇿 Uz':
        xabar = t.translate(text=txt, dest='uz').text
        await message.answer(xabar, reply_markup=voice)
        speech(mytext=xabar, lan='tr')
    elif tarjima == '🇺🇿 Uz -> 🇬🇧 En':
        xabar = t.translate(text=txt, dest='en').text
        await message.answer(xabar, reply_markup=voice)
        speech(mytext=xabar, lan='en')
    elif tarjima == '🇬🇧 En -> 🇺🇿 Uz':
        xabar = t.translate(text=txt, dest='uz').text
        await message.answer(xabar, reply_markup=voice)
        speech(mytext=xabar, lan='tr')
    await state.set_state(Translate_bot.voice)


@dp.callback_query(Translate_bot.voice)
async def get_voice(call: CallbackQuery, state: FSMContext):
    audio = FSInputFile('audio.mp3')
    await bot.send_audio(call.message.chat.id, audio)
    os.remove('audio.mp3')
    await state.clear()  
    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        print("bot o`chdi")        