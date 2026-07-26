from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Image to PDF"),
            KeyboardButton(text="PDF to DOCX"),
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Choose a service...",
)
