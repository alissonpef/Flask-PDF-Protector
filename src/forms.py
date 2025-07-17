from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, SubmitField, ColorField, IntegerField, RadioField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class UploadForm(FlaskForm):
    watermark_type = RadioField(
        'Tipo de Marca d\'água',
        choices=[('text', 'Texto'), ('image', 'Imagem')],
        default='text'
    )

    cpf = StringField('Texto (CPF, Nome, etc.)', validators=[Optional(), Length(min=2, max=50)])
    color = ColorField('Cor do Texto', default='#c0c0c0')
    font_size = IntegerField('Tamanho da Fonte', default=12, validators=[NumberRange(min=6, max=72)])

    watermark_image = FileField(
        'Arquivo de Imagem (PNG recomendado)',
        validators=[Optional(), FileAllowed(['png', 'jpg', 'jpeg'], 'Apenas imagens PNG ou JPG!')]
    )

    opacity = IntegerField('Opacidade (0-100)', default=15, validators=[NumberRange(min=0, max=100)])
    position = SelectField(
        'Posição/Estilo',
        choices=[
            ('diagonal', 'Diagonal Repetida'),
            ('center', 'Centralizado'),
            ('bottom-right', 'Rodapé Direito')
        ],
        default='diagonal'
    )

    file = FileField('Escolher arquivo PDF', validators=[DataRequired(), FileAllowed(['pdf'])])
    submit = SubmitField('Proteger PDF')
