from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp


class UploadForm(FlaskForm):
    watermark_type = RadioField(
        "Watermark Type",
        choices=[("text", "Text"), ("image", "Image")],
        default="text",
        validators=[DataRequired()],
    )

    watermark_text = StringField(
        "Watermark Text (e.g., Name, ID)",
        validators=[
            Optional(),
            Length(min=2, max=35, message="Text must be between 2 and 35 characters."),
        ],
    )

    font_size = IntegerField(
        "Font Size", default=12, validators=[Optional(), NumberRange(min=6, max=72)]
    )

    color = StringField(
        "Font Color",
        default="#c0c0c0",
        validators=[
            Optional(),
            Regexp(
                r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$", message="Invalid color code."
            ),
        ],
    )

    watermark_image = FileField(
        "Image File (PNG recommended)",
        validators=[Optional(), FileAllowed(["png", "jpg", "jpeg"], "Images only!")],
    )

    opacity = IntegerField(
        "Opacity (1-100)",
        default=75,
        validators=[
            DataRequired(),
            NumberRange(min=1, max=100, message="Opacity must be between 1 and 100."),
        ],
    )

    position = SelectField(
        "Position/Style",
        choices=[
            ("diagonal", "Diagonal Tiling"),
            ("bottom-right", "Bottom Right"),
        ],
        default="diagonal",
        validators=[DataRequired()],
    )

    pdf_file = FileField(
        "PDF File", validators=[FileRequired(), FileAllowed(["pdf"], "PDFs only!")]
    )

    submit = SubmitField("Protect PDF")
