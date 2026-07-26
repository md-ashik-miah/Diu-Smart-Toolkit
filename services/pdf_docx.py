from pdf2docx import Converter


def convert_pdf_to_docx(pdf_path: str, docx_path: str) -> None:
    """Convert a PDF while retaining its layout where the source allows it."""
    converter = Converter(pdf_path)
    try:
        converter.convert(docx_path, start=0, end=None)
    finally:
        converter.close()
