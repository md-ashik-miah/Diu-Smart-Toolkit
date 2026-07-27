import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers.commands.start import router as start_router
from handlers.commands.info import router as info_router
from handlers.pdf.image_to_pdf import router as image_router
from handlers.pdf.pdf_to_docx import router as pdf_to_docx_router


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(info_router)
    dp.include_router(image_router)
    dp.include_router(pdf_to_docx_router)

    print("✅ Bot is running...")
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Start the bot"),
            BotCommand(command="help", description="All commands"),
            BotCommand(command="about", description="About this bot"),
        ]
    )


if __name__ == "__main__":
    asyncio.run(main())
