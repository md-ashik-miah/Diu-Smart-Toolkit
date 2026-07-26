from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "Available commands:\n\n"
        "/start - Show the main menu\n"
        "/help - Show all commands\n"
        "/about - Learn about this bot\n\n"
        "Use the menu to convert images to PDF or PDF to DOCX."
    )


@router.message(Command("about"))
async def about_command(message: Message):
    await message.answer(
        "Document Converter Bot creates PDFs from images and converts PDFs to DOCX."
    )
