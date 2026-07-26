from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

image_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Generate PDF")],
        [KeyboardButton(text="Cancel")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Send your images...",
)
