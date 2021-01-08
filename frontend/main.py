import os
from os.path import dirname

from flask import Flask, render_template, request
from flask_socketio import SocketIO

from backend.game import Game


template_dir = os.path.join(dirname(__file__), 'templates')
static_dir = os.path.join(dirname(__file__), 'static')
app = Flask(__name__, template_folder=template_dir, static_url_path=static_dir)
socket_io = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/show_board', methods=['POST'])
def show_board():
    if request.method == 'POST':
        board = app.game.get_board()
        socket_io.emit('board_display', board)
    return render_template('index.html')


if __name__ == '__main__':
    app.url_base = 'localhost'
    app.port = 5000
    app.game = Game(socket_io)
    socket_io.run(app, host=app.url_base, port=app.port, debug=True)

