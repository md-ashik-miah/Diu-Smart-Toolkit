from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PIL import Image
import img2pdf
import os

PAGE_WIDTH, PAGE_HEIGHT = A4


def create_pdf(image_paths, output_path, mode="a4"):
    """
    mode:
        a4        -> Every image is fitted to an A4 page.
        original  -> Keep original image size.
    """

    if mode == "original":
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(image_paths))
        return

    # ---------- A4 Mode ----------
    pdf = canvas.Canvas(output_path, pagesize=A4)

    margin = 20

    for image_path in image_paths:

        img = Image.open(image_path)
        img = img.convert("RGB")

        img_width, img_height = img.size

        available_width = PAGE_WIDTH - (2 * margin)
        available_height = PAGE_HEIGHT - (2 * margin)

        scale = min(
            available_width / img_width,
            available_height / img_height
        )

        new_width = img_width * scale
        new_height = img_height * scale

        x = (PAGE_WIDTH - new_width) / 2
        y = (PAGE_HEIGHT - new_height) / 2

        pdf.drawImage(
            image_path,
            x,
            y,
            width=new_width,
            height=new_height,
            preserveAspectRatio=True,
            mask="auto"
        )

        pdf.showPage()

    pdf.save()