from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import main_menu

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "Document Converter Bot\n\n"
        "Convert images to PDF or a PDF file to an editable DOCX document.\n"
        "",
        reply_markup=main_menu,
    )
