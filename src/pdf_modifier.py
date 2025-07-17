from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os

def modify_pdf(filename, upload_folder, watermark_type, **kwargs):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    width, height = A4

    opacity = kwargs.get('opacity', 15)
    position = kwargs.get('position', 'diagonal')

    can.setFillAlpha(opacity / 100.0)

    if watermark_type == 'image' and 'watermark_image_path' in kwargs:
        img_path = kwargs['watermark_image_path']
        try:
            img = ImageReader(img_path)
            img_width, img_height = img.getSize()
            aspect = img_height / float(img_width)

            display_width = 150
            display_height = display_width * aspect

            if position == 'center':
                x_center = (width - display_width) / 2
                y_center = (height - display_height) / 2
                can.drawImage(img, x_center, y_center, width=display_width, height=display_height, mask='auto')
            else:
                can.translate(width / 2, height / 2)
                can.rotate(45)
                for x in range(-int(width), int(width), int(display_width + 100)):
                    for y in range(-int(height), int(height), int(display_height + 100)):
                        can.drawImage(img, x, y, width=display_width, height=display_height, mask='auto')

        except Exception as e:
            raise ValueError(f"Não foi possível processar a imagem: {e}")

    elif watermark_type == 'text' and 'text' in kwargs:
        text = kwargs.get('text', '')
        font_size = kwargs.get('font_size', 12)
        color = kwargs.get('color', '#c0c0c0')

        can.setFont("Helvetica", font_size)
        can.setFillColor(HexColor(color))

        if position == 'diagonal':
            text_to_repeat = f"{text} " * 5
            can.translate(width / 2, height / 2)
            can.rotate(45)
            for x in range(-int(width), int(width), 250):
                for y in range(-int(height), int(height), 100):
                    can.drawString(x, y, text_to_repeat)
        else:
            positions = {'bottom-right': (450, 50), 'center': (200, 400)}
            x, y = positions.get(position, (450, 50))
            can.drawString(x, y, text)

    can.save()
    packet.seek(0)
    watermark_pdf = PdfReader(packet)
    watermark_page = watermark_pdf.pages[0]

    original_pdf_path = os.path.join(upload_folder, filename)
    output_filename = f"protected_{filename}"
    output_path = os.path.join(upload_folder, output_filename)

    with open(original_pdf_path, "rb") as original_file:
        existing_pdf = PdfReader(original_file)
        output = PdfWriter()

        for page in existing_pdf.pages:
            page.merge_page(watermark_page)
            output.add_page(page)

        with open(output_path, "wb") as outputStream:
            output.write(outputStream)

    return output_filename
