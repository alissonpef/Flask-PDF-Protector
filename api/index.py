import os
from flask import Flask, render_template, flash
from dotenv import load_dotenv
from .forms import UploadForm

project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
dotenv_path = os.path.join(project_folder, ".env")
load_dotenv(dotenv_path)

app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY", "a-default-secret-key-for-development"
)


@app.route("/", methods=["GET", "POST"])
def home():
    form = UploadForm()
    if form.validate_on_submit():
        flash("Form submitted successfully!")

    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
