from flask import Flask, render_template, jsonify, request, send_from_directory, url_for
from PIL import Image, UnidentifiedImageError
import logging
import uuid
import os
from io import BytesIO
from pathlib import Path

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent

IMAGES_DIR = Path("IMAGES_DIR", BASE_DIR / 'images')

LOGS_DIR = Path("LOGS_DIR", BASE_DIR / 'logs')

MAX_FILE_SIZE = 5 * 1024 * 1024

REQUEST_LIMIT = MAX_FILE_SIZE + 1024 * 1024

ALLOWED_IMAGE_FORMAT = {
    'JPEG': 'jpg',
    'PNG': 'png',
    'GIF': 'gif'
}
app.config['MAX_CONTENT_LENGTH'] = REQUEST_LIMIT
IMAGES_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOGS_DIR / 'app.log',
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s]',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)


def detect_image_extension(file_data: bytes):
    try:
        with Image.open(BytesIO(file_data)) as image:
            image.verify()

            return ALLOWED_IMAGE_FORMAT.get(image.format)
    except (UnidentifiedImageError, OSError) as e:
        return None


@app.get('/')
def home():
    return render_template("index.html")


@app.get('/upload')
def upload_page():
    return render_template("upload.html")


@app.get('/images/')
def images_page():
    images = []
    for image_path in sorted(IMAGES_DIR.iterdir(), key=lambda path: path.stat().st_mtime, reverse=True):
        if not image_path.is_file():
            continue
        relative_url = url_for('get_image', filename=image_path.name)
        full_url = request.host_url.rstrip('/') + relative_url
        images.append(
            {
                'name': image_path.name,
                'url': relative_url,
                'full_url': full_url
            }
        )
    return render_template("images.html", images=images)


@app.get('/me')
def get_me_account():
    info = {
        'id': 1,
        'name': 'John',
        'age': 67,
        'place_work': 'idk',
        'languages': ['python', 'java', 'CSS'],
        'Iaadult': False,
        'adress': {
            'city': 'Rostov-on-Don',
            'Street': 'sss',
        }
    }
    return render_template("me/home.html", info=info)


@app.post('/upload')
def upload_image():
    uploaded_file = request.files.get('image')
    if uploaded_file is None:
        logging.warning("Ошибка: файл image не найден в запросе")
        return jsonify(
            {
                'error': 'Файл не найден. Поле формы должно называться image.'
            }
        )
    original_filename = uploaded_file.filename or 'unknown'
    file_data = uploaded_file.read()
    if not file_data:
        logging.warning(f"Ошибка: файл пустой {original_filename}")
        return jsonify(
            {
                'error': 'Файл пустой.'
            }
        ), 400
    if len(file_data) > MAX_FILE_SIZE:
        logging.warning(f"Ошибка: файл {original_filename} не должен быть больше 5 МБ.")
        return jsonify(
            {
                'error': 'Файл не должен быть больше 5 МБ.'
            }
        )
    image_extension = detect_image_extension(file_data)
    if image_extension is None:
        logging.warning(f"Ошибка: неподдерживаемый или поврежденный файл.")
        return jsonify(
            {
                'error': 'Поддерживаются только форматы jpg,png,gif.'
            }
        )
    unique_filename = f'{uuid.uuid4().hex}.{image_extension}'
    target_path = IMAGES_DIR / unique_filename
    target_path.write_bytes(file_data)

    print("SAVE PATH:", target_path)
    print("EXISTS:", target_path.exists())
    print("SIZE:", target_path.stat().st_size if target_path.exists() else "NO FILE")


    relative_url = url_for('get_image', filename=unique_filename)
    full_url = request.host_url.rstrip('/') + relative_url

    logging.info(f'Успех.Изображение загружено как {original_filename}')
    return jsonify(
        {
            'message': 'Изображение успешно загружено',
            'id': unique_filename,
            'url': relative_url,
            'full_url': full_url
        }
    ), 201


@app.get('/images/<path:filename>')
def get_image(filename):
    return send_from_directory(str(IMAGES_DIR), filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3001, debug=False)
