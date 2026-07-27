import os
import shutil
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from handlers.commands.cancel import cancel_pdf as cancel_operation
from keyboards.image_menu import image_menu
from keyboards.main_menu import main_menu
from keyboards.pdf_size_menu import pdf_size_menu
from services.image_pdf import create_pdf
from states.image_state import ImageToPDF

router = Router()


@router.message(F.text == "Image to PDF")
async def image_to_pdf_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ImageToPDF.choosing_size)
    await message.answer("Select the PDF page size:", reply_markup=pdf_size_menu)


@router.message(ImageToPDF.choosing_size, F.text == "A4 (Default)")
async def choose_a4(message: Message, state: FSMContext):
    await begin_image_upload(message, state, "a4", "A4")


@router.message(ImageToPDF.choosing_size, F.text == "Original Size")
async def choose_original(message: Message, state: FSMContext):
    await begin_image_upload(message, state, "original", "Original-size")


async def begin_image_upload(
    message: Message, state: FSMContext, pdf_mode: str, label: str
):
    folder = os.path.join("temp", str(message.from_user.id))
    os.makedirs(folder, exist_ok=True)
    await state.update_data(images=[], pdf_mode=pdf_mode)
    await state.set_state(ImageToPDF.waiting_for_images)
    await message.answer(
        f"{label} mode selected. Send one or more images, then press Generate PDF.\n\nFor maintain page serial, Send Image One By One For serially.",
        reply_markup=image_menu,
    )


@router.message(ImageToPDF.waiting_for_images, F.photo)
async def receive_image(message: Message, state: FSMContext):
    folder = os.path.join("temp", str(message.from_user.id))
    os.makedirs(folder, exist_ok=True)

    photo = message.photo[-1]
    file_path = os.path.join(folder, f"{photo.file_unique_id}.jpg")
    await message.bot.download(photo, destination=file_path)

    data = await state.get_data()
    images = data.get("images", [])
    images.append(file_path)
    await state.update_data(images=images)
    await message.answer(f"Image received. Total images: {len(images)}")


@router.message(ImageToPDF.waiting_for_images, F.text == "Generate PDF")
async def finish_pdf(message: Message, state: FSMContext):
    data = await state.get_data()
    images = data.get("images", [])
    if not images:
        await message.answer("Please send at least one image.")
        return

    folder = os.path.join("temp", str(message.from_user.id))
    pdf_path = os.path.join(
        folder, datetime.now().strftime("images_%Y%m%d_%H%M%S.pdf")
    )

    try:
        create_pdf(images, pdf_path, data.get("pdf_mode", "a4"))
        await message.answer_document(
            FSInputFile(pdf_path), caption="PDF created successfully."
        )
    except Exception:
        await message.answer("The PDF could not be created. Please try again.")
    finally:
        shutil.rmtree(folder, ignore_errors=True)
        await state.clear()
        await message.answer("Ready to create another PDF.", reply_markup=main_menu)


@router.message(ImageToPDF.choosing_size, F.text == "Cancel")
@router.message(ImageToPDF.waiting_for_images, F.text == "Cancel")
async def cancel_pdf(message: Message, state: FSMContext):
    await cancel_operation(message, state)
