import asyncio
import os
import shutil
from datetime import datetime

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, Message

from handlers.commands.cancel import cancel_pdf as cancel_operation
from keyboards.cancel_menu import cancel_menu
from keyboards.main_menu import main_menu
from services.pdf_docx import convert_pdf_to_docx
from states.document_state import PdfToDocx

router = Router()


@router.message(F.text == "PDF to DOCX")
async def pdf_to_docx_start(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(PdfToDocx.waiting_for_pdf)
    await message.answer(
        "Send a PDF file and I will convert it to an editable DOCX document.\n\n"
        "For the best result, use a text-based PDF; scanned PDFs may need OCR first.",
        reply_markup=cancel_menu,
    )


@router.message(
    PdfToDocx.waiting_for_pdf,
    F.document,
    F.document.file_name.lower().endswith(".pdf"),
)
async def convert_uploaded_pdf(message: Message, state: FSMContext):
    folder = os.path.join("temp", str(message.from_user.id))
    os.makedirs(folder, exist_ok=True)

    input_path = os.path.join(folder, f"{message.document.file_unique_id}.pdf")
    output_path = os.path.join(
        folder, datetime.now().strftime("converted_%Y%m%d_%H%M%S.docx")
    )

    await message.answer("Converting your PDF to DOCX. This may take a moment...")

    try:
        await message.bot.download(message.document, destination=input_path)
        await asyncio.to_thread(convert_pdf_to_docx, input_path, output_path)
        await message.answer_document(
            FSInputFile(output_path), caption="DOCX created successfully."
        )
    except Exception:
        await message.answer(
            "This PDF could not be converted. Please try another PDF file."
        )
    finally:
        shutil.rmtree(folder, ignore_errors=True)
        await state.clear()
        await message.answer("Ready to convert another document.", reply_markup=main_menu)


@router.message(PdfToDocx.waiting_for_pdf, F.text == "Cancel")
async def cancel_pdf_to_docx(message: Message, state: FSMContext):
    await cancel_operation(message, state)


@router.message(PdfToDocx.waiting_for_pdf, F.document)
async def non_pdf_document(message: Message):
    await message.answer("Please send a PDF file, or tap Cancel to return to the menu.")
