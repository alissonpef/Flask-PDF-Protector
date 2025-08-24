from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from io import BytesIO


def add_watermark(pdf_stream, watermark_type, **kwargs):

    pdf_reader = PdfReader(pdf_stream)
    pdf_writer = PdfWriter()

    watermark_packet = BytesIO()
    can = canvas.Canvas(watermark_packet, pagesize=letter)
    width, height = letter

    opacity = kwargs.get("opacity", 15) / 100.0
    can.setFillAlpha(opacity)

    if watermark_type == "image" and "image_stream" in kwargs:
        image_stream = kwargs.get("image_stream")
        try:
            watermark_image = ImageReader(image_stream)
            img_width, img_height = watermark_image.getSize()
            aspect = img_height / float(img_width)
            display_width = 150
            display_height = display_width * aspect

            if kwargs.get("position") == "center":
                x_center = (width - display_width) / 2
                y_center = (height - display_height) / 2
                can.drawImage(
                    watermark_image,
                    x_center,
                    y_center,
                    width=display_width,
                    height=display_height,
                    mask="auto",
                )
            else:
                can.translate(width / 2, height / 2)
                can.rotate(45)
                for x in range(-int(width), int(width), int(display_width + 100)):
                    for y in range(
                        -int(height), int(height), int(display_height + 100)
                    ):
                        can.drawImage(
                            watermark_image,
                            x,
                            y,
                            width=display_width,
                            height=display_height,
                            mask="auto",
                        )
        except Exception as e:
            raise ValueError(f"Could not process the image file: {e}")

    elif watermark_type == "text" and "text" in kwargs:
        text = kwargs.get("text", "")
        font_size = kwargs.get("font_size", 12)
        can.setFont("Helvetica", font_size)
        can.setFillColor(HexColor("#c0c0c0"))

        if kwargs.get("position") == "center":
            can.drawCentredString(width / 2, height / 2, text)
        else:
            text_to_repeat = f"{text} " * 5
            can.translate(width / 2, height / 2)
            can.rotate(45)
            for x in range(-int(width), int(width), 250):
                for y in range(-int(height), int(height), 100):
                    can.drawString(x, y, text_to_repeat)

    can.save()
    watermark_packet.seek(0)
    watermark_pdf = PdfReader(watermark_packet)
    watermark_page = watermark_pdf.pages[0]

    for page in pdf_reader.pages:
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    final_pdf_packet = BytesIO()
    pdf_writer.write(final_pdf_packet)
    final_pdf_packet.seek(0)

    return final_pdf_packet
