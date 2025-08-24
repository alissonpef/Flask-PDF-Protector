from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, Color, toColor
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image


def add_watermark(pdf_stream, watermark_type, **kwargs):
    opacity_value = kwargs.get("opacity", 15)
    if opacity_value <= 0:
        pdf_stream.seek(0)
        final_pdf_packet = BytesIO(pdf_stream.read())
        final_pdf_packet.seek(0)
        return final_pdf_packet

    pdf_reader = PdfReader(pdf_stream)
    pdf_writer = PdfWriter()

    watermark_packet = BytesIO()
    can = canvas.Canvas(watermark_packet, pagesize=letter)
    width, height = letter

    opacity_float = opacity_value / 100.0
    position = kwargs.get("position", "diagonal")

    if watermark_type == "image" and "image_stream" in kwargs:
        try:
            image_stream = kwargs.get("image_stream")
            img = Image.open(image_stream).convert("RGBA")
            img_with_opacity = Image.new("RGBA", img.size)
            img_with_opacity = Image.blend(img_with_opacity, img, opacity_float)
            temp_image_stream = BytesIO()
            img_with_opacity.save(temp_image_stream, format="PNG")
            temp_image_stream.seek(0)
            watermark_image = ImageReader(temp_image_stream)
            img_width, img_height = watermark_image.getSize()
            aspect = img_height / float(img_width)
            display_width = 150
            display_height = display_width * aspect

            if position == "bottom-right":
                can.drawImage(
                    watermark_image,
                    400,
                    50,
                    width=display_width,
                    height=display_height,
                    mask="auto",
                )
            else:
                can.translate(width / 2, height / 2)
                can.rotate(45)
                for x in range(
                    -int(width * 1.5), int(width * 1.5), int(display_width + 100)
                ):
                    for y in range(
                        -int(height * 1.5), int(height * 1.5), int(display_height + 100)
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
        if not text.strip():
            pdf_stream.seek(0)
            return pdf_stream

        font_size = kwargs.get("font_size", 12)
        font_name = "Helvetica-Bold"
        can.setFont(font_name, font_size)

        color_hex = kwargs.get("color", "#c0c0c0")
        base_color = toColor(color_hex)

        final_color_with_opacity = Color(
            base_color.red, base_color.green, base_color.blue, alpha=opacity_float
        )

        can.setFillColor(final_color_with_opacity)

        if position == "bottom-right":
            can.drawRightString(width - 50, 50, text)
        else:  # Diagonal
            can.translate(width / 2, height / 2)
            can.rotate(45)

            single_text_width = can.stringWidth(text, font_name, font_size)
            horizontal_spacing = 150
            vertical_spacing = 120
            step_x = single_text_width + horizontal_spacing

            for y in range(-int(height * 2), int(height * 2), vertical_spacing):
                for x in range(-int(width * 2), int(width * 2), int(step_x)):
                    can.drawString(x, y, text)

    can.save()
    watermark_packet.seek(0)

    if watermark_packet.getbuffer().nbytes == 0:
        pdf_stream.seek(0)
        return pdf_stream

    watermark_pdf = PdfReader(watermark_packet)
    if not watermark_pdf.pages:
        pdf_stream.seek(0)
        return pdf_stream

    watermark_page = watermark_pdf.pages[0]
    for page in pdf_reader.pages:
        page.merge_page(watermark_page)
        pdf_writer.add_page(page)

    final_pdf_packet = BytesIO()
    pdf_writer.write(final_pdf_packet)
    final_pdf_packet.seek(0)
    return final_pdf_packet
