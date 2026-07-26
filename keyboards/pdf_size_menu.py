from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

pdf_size_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="A4 (Default)"), KeyboardButton(text="Original Size")],
        [KeyboardButton(text="Cancel")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Select PDF page size...",
)
