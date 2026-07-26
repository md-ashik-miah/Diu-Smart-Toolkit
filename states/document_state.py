from aiogram.fsm.state import State, StatesGroup


class PdfToDocx(StatesGroup):
    waiting_for_pdf = State()
