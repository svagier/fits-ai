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


@app.route('/game_setup', methods=['GET', 'POST'])
def game_setup():
    if request.method == 'POST':
        game_data = {
            "field_size": 20,
            "field_offset": 2,
            "tallest_block_height": 4  # TODO add dynamic
        }
        socket_io.emit('game_setup', game_data)
    return render_template('index.html')


@app.route('/show_board', methods=['POST'])
def show_board():
    if request.method == 'POST':
        board = app.game.get_board()
        socket_io.emit('board_display', board)
    return render_template('index.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    if request.method == 'POST':
        run_game_and_send_to_front()
    return render_template('index.html')


def run_game_and_send_to_front():
    for turn_dict in app.game.run_game():
        socket_io.emit('current_block', turn_dict['current_block'])
        print('turn_data', turn_dict)


if __name__ == '__main__':
    app.url_base = 'localhost'
    app.port = 5000
    app.game = Game(socket_io)
    socket_io.run(app, host=app.url_base, port=app.port, debug=True)
