from aiogram.fsm.state import State, StatesGroup


class ProfileStates(StatesGroup):
    name = State()
    age = State()
    specialization = State()
    help_text = State()
    message = State()
