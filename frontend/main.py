from os.path import dirname

from flask import Flask, render_template
from flask_socketio import SocketIO

template_dir = dirname(__file__)
app = Flask(__name__, template_folder=template_dir)
socket_io = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    app.url_base = 'localhost'
    app.port = 5000
    socket_io.run(app, host=app.url_base, port=app.port, debug=True)
