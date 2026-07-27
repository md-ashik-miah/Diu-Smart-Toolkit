import asyncio
import os
from aiohttp import web

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers.commands.start import router as start_router
from handlers.commands.info import router as info_router
from handlers.pdf.image_to_pdf import router as image_router
from handlers.pdf.pdf_to_docx import router as pdf_to_docx_router


# --- 1. Define the Dummy Web Server for Render ---
async def handle_ping(request):
    return web.Response(text="Bot is running!")

async def web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render binds to a specific PORT environment variable dynamically
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"Web server successfully started on port {port}")
# -------------------------------------------------


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

    # --- 2. Run both the Web Server and the Bot Polling concurrently ---
    # This prevents the script from exiting and satisfies Render's port rules.
    await asyncio.gather(
        web_server(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())
