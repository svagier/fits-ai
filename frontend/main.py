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


@app.route('/game_setup', methods=['POST'])
def game_setup():
    if request.method == 'POST':
        game_data = {
            "number_of_columns": app.game.board_width,
            "field_size": 20,
            "field_offset": 2,
            "tallest_block_height": 4,  # TODO add dynamic
            "widest_block_width": 4     # TODO add dynamic
        }
        socket_io.emit('game_setup', game_data)
    return render_template('index.html')


@app.route('/show_board', methods=['POST'])
def show_board():
    if request.method == 'POST':
        board = app.game.get_board()
        socket_io.emit('board_display', board.tolist())
    return render_template('index.html')


@app.route('/can_place_block', methods=['POST'])
def can_place_block():
    if request.method == 'POST':
        response_json = request.get_json()
        rotation_index = response_json['rotation_index']
        start_column = response_json['start_column']
        block_to_be_placed = app.game.current_shape[rotation_index]
        if app.game.player_place_block(start_column, block_to_be_placed):
            socket_io.emit('board_display', app.game.get_board().tolist())
            next_turn()
    return render_template('index.html')


@app.route('/reject_current_block', methods=['POST'])
def reject_current_block():
    next_turn()
    return render_template('index.html')


@app.route('/start_game', methods=['POST'])
def start_game():
    if request.method == 'POST':
        app.game = Game()
        next_turn()
    return render_template('index.html')


def next_turn():
    turn_dict = app.game.next_turn()
    # if turn_dict['is_finish']:
        # TODO
    if 'new_shape' in turn_dict.keys() and turn_dict['new_shape']:
        socket_io.emit('current_shape', turn_dict['new_shape'])
    if 'remaining_shapes' in turn_dict.keys() and turn_dict['remaining_shapes']:
        socket_io.emit('remaining_shapes', turn_dict['remaining_shapes'])

# def run_game_and_send_to_front():
#     for turn_dict in app.game.run_game():
#         socket_io.emit('current_shape', [nparray.tolist() for nparray in turn_dict['current_shape']])
#         # print('turn_data', turn_dict)


if __name__ == '__main__':
    app.url_base = 'localhost'
    app.port = 5000
    app.game = Game()
    socket_io.run(app, host=app.url_base, port=app.port, debug=True)
