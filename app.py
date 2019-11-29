import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = os.environ.get('SECRET')
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/controls/<int:id>')
def controls(id):
    return render_template('controls.html', id=id)


@app.route('/<int:id>')
def viewer(id):
    return render_template('viewer.html', id=id)


@socketio.on('connection')
def connection(data):
    print(data)
    emit('deliver_slides', broadcast=True)


@socketio.on('deliver_slides_received')
def slide_delivery(data):
    print(data)
    emit('slide_delivery', data, broadcast=True)


@socketio.on('slide')
def slide(data):
    print(data)
    emit('slide_change', data, broadcast=True)
    print('sent slide change')


if __name__ == '__main__':
    socketio.run(app, debug=True)
