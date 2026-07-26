from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

cancel_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Cancel")]],
    resize_keyboard=True,
    input_field_placeholder="Send a PDF file...",
)
