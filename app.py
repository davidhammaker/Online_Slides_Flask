import os
from flask import Flask, render_template, redirect, url_for
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from forms import FilesForm
import requests
from datetime import datetime
from io import BytesIO
from PIL import Image


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET')
socketio = SocketIO(app)

backend_url = os.environ.get('OSLIDES_BE_URL')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = FilesForm()
    if form.validate_on_submit():
        new_slideshow = requests.post(
            f'{backend_url}slideshows/',
            data={'name': f'slideshow {datetime.now()}'}
        )
        slideshow_id = new_slideshow.json()['id']
        print(slideshow_id)
        print(form.files.data)
        files = sorted(
            form.files.data,
            key=lambda file: file.filename
        )
        for file in files:
            print(file.stream)
            img_bytes = BytesIO(file.stream.read())
            img = Image.open(img_bytes)
            img.save(f'{file.filename}')
            files = {'image': open(f'{file.filename}', 'rb')}
            data = {'slideshow': slideshow_id}
            new_slide = requests.post(
                f'{backend_url}slideshows/{slideshow_id}/',
                files=files,
                data=data
            )
            print(new_slide)
            print(new_slide.json())
            os.remove(f'{file.filename}')
        return redirect(url_for('slideshow', id=slideshow_id))
    else:
        print('error')
    return render_template('upload.html', form=form)


@app.route('/controls/<int:id>')
def controls(id):
    return render_template('controls.html', id=id, url=backend_url)


@app.route('/<int:id>')
def viewer(id):
    return render_template('viewer.html', id=id)


@app.route('/slideshow/<int:id>')
def slideshow(id):
    return render_template('slideshow.html', id=id)


@socketio.on('connection')
def connection(data):
    emit('deliver_slides', broadcast=True)


@socketio.on('deliver_slides_received')
def slide_delivery(data):
    emit('slide_delivery', data, broadcast=True)


@socketio.on('slide')
def slide(data):
    emit('slide_change', data, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
