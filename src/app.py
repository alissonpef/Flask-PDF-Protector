import os
from flask import Flask, render_template, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from forms import UploadForm
from pdf_modifier import modify_pdf

project_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
dotenv_path = os.path.join(project_folder, '.env')
load_dotenv(dotenv_path=dotenv_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

basedir = os.path.abspath(os.path.dirname(__file__))
upload_folder = os.path.join(basedir, 'uploads')
app.config['UPLOAD_FOLDER'] = upload_folder
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    download_url = None

    if form.validate_on_submit():
        pdf_file = form.file.data
        pdf_filename = secure_filename(pdf_file.filename)
        pdf_file_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        pdf_file.save(pdf_file_path)

        watermark_params = {
            'opacity': form.opacity.data,
            'position': form.position.data
        }

        watermark_type = form.watermark_type.data

        if watermark_type == 'text':
            watermark_params['text'] = form.cpf.data
            watermark_params['font_size'] = form.font_size.data
            watermark_params['color'] = form.color.data

        elif watermark_type == 'image':
            image_file = form.watermark_image.data
            if image_file:
                image_filename = secure_filename(image_file.filename)
                image_file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image_file.save(image_file_path)
                watermark_params['watermark_image_path'] = image_file_path
            else:
                flash('Por favor, selecione um arquivo de imagem para a marca d\'água.')
                return render_template('index.html', form=form, download_url=None)

        try:
            new_filename = modify_pdf(
                filename=pdf_filename,
                upload_folder=app.config['UPLOAD_FOLDER'],
                watermark_type=watermark_type,
                **watermark_params
            )
            flash('Seu PDF foi protegido com sucesso!')
            download_url = url_for('download', filename=new_filename)
        except Exception as e:
            flash(f'Ocorreu um erro ao processar o PDF: {e}')

    return render_template('index.html', form=form, download_url=download_url)


@app.route('/uploads/<filename>')
def download(filename):
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        filename,
        as_attachment=True
    )


if __name__ == '__main__':
    app.run(debug=True)
