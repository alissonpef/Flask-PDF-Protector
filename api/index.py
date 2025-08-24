import os
from flask import Flask, render_template, flash, send_file, url_for
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from .forms import UploadForm
from .pdf_utils import add_watermark
from io import BytesIO

project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(project_folder, ".env")
load_dotenv(dotenv_path)

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "a-default-secret-key-for-development"
)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        pdf_file = form.pdf_file.data
        watermark_type = form.watermark_type.data

        watermark_params = {
            "opacity": form.opacity.data,
            "position": form.position.data,
        }

        if watermark_type == "text":
            watermark_params["text"] = form.watermark_text.data
            watermark_params["font_size"] = form.font_size.data
            watermark_params["color"] = form.color.data

        elif watermark_type == "image":
            image_file = form.watermark_image.data
            if not image_file:
                flash("Please select an image file for the watermark.", "error")
                return render_template("index.html", form=form)
            watermark_params["image_stream"] = image_file.stream

        pdf_bytes_content = pdf_file.read()
        pdf_stream_for_processing = BytesIO(pdf_bytes_content)

        try:
            output_pdf_stream = add_watermark(
                pdf_stream_for_processing, watermark_type, **watermark_params
            )

            original_filename = secure_filename(pdf_file.filename)
            download_filename = f"protected_{original_filename}"

            return send_file(
                output_pdf_stream,
                as_attachment=True,
                download_name=download_filename,
                mimetype="application/pdf",
            )

        except Exception as e:
            flash(f"An error occurred while processing the PDF: {e}", "error")

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
