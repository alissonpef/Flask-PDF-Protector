from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SelectField, SubmitField, RadioField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class UploadForm(FlaskForm):
    watermark_type = RadioField(
        "Watermark Type",
        choices=[("text", "Text"), ("image", "Image")],
        default="text",
        validators=[DataRequired()],
    )

    watermark_text = StringField(
        "Watermark Text (e.g., Name, ID)",
        validators=[Optional(), Length(min=2, max=50)],
    )
    font_size = IntegerField(
        "Font Size", default=12, validators=[Optional(), NumberRange(min=6, max=72)]
    )

    watermark_image = FileField(
        "Image File (PNG recommended)",
        validators=[Optional(), FileAllowed(["png", "jpg", "jpeg"], "Images only!")],
    )

    opacity = IntegerField(
        "Opacity (0-100)",
        default=15,
        validators=[DataRequired(), NumberRange(min=0, max=100)],
    )
    position = SelectField(
        "Position/Style",
        choices=[
            ("diagonal", "Diagonal Tiling"),
            ("center", "Center"),
        ],
        default="diagonal",
        validators=[DataRequired()],
    )

    pdf_file = FileField(
        "PDF File", validators=[FileRequired(), FileAllowed(["pdf"], "PDFs only!")]
    )

    submit = SubmitField("Protect PDF")
