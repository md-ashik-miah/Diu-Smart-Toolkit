from aiogram.fsm.state import StatesGroup, State

class ImageToPDF(StatesGroup):
    choosing_size = State()
    waiting_for_images = State()