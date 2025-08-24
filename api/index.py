import os

from flask import Flask, flash, render_template, send_file
from werkzeug.utils import secure_filename

from .forms import UploadForm
from .pdf_utils import add_watermark

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = os.urandom(24)


@app.route("/", methods=["GET", "POST"])
def index():
    form = UploadForm()
    if form.validate_on_submit():
        pdf_file = form.pdf_file.data
        watermark_type = form.watermark_type.data

        kwargs = {
            "opacity": form.opacity.data,
            "position": form.position.data,
        }

        if watermark_type == "text":
            if not form.watermark_text.data:
                flash("Watermark text is required for text type.", "error")
                return render_template("index.html", form=form)
            kwargs["text"] = form.watermark_text.data
            kwargs["font_size"] = form.font_size.data
            kwargs["color"] = form.color.data

        elif watermark_type == "image":
            image_file = form.watermark_image.data
            if not image_file:
                flash("An image file is required for image type.", "error")
                return render_template("index.html", form=form)
            kwargs["image_stream"] = image_file.stream

        try:
            final_pdf = add_watermark(
                pdf_stream=pdf_file.stream,
                watermark_type=watermark_type,
                **kwargs,
            )

            safe_filename = secure_filename(pdf_file.filename)
            new_filename = f"protected_{safe_filename}"

            return send_file(
                final_pdf,
                as_attachment=True,
                download_name=new_filename,
                mimetype="application/pdf",
            )
        except Exception as e:
            flash(f"An error occurred: {e}", "error")

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
