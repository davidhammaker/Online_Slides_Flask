import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
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


@socketio.on('my event')
def test_message(message):
    emit('my response', {'data': 'got it!'})
    print(message)


if __name__ == '__main__':
    socketio.run(app, debug=True)
