from aiogram.fsm.state import StatesGroup, State

class Translate_bot(StatesGroup):
    lang = State()
    trans = State()
    voice = State()
    