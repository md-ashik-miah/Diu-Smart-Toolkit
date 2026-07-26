import os
import shutil

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.main_menu import main_menu


async def cancel_pdf(message: Message, state: FSMContext) -> None:
    shutil.rmtree(os.path.join("temp", str(message.from_user.id)), ignore_errors=True)
    await state.clear()
    await message.answer(
        "Operation canceled ❌.\n\nPlease choose a service to continue...",
        reply_markup=main_menu,
    )
