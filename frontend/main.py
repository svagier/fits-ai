import eventlet

from backend.boards import BoardManager

eventlet.monkey_patch()

import os
from os.path import dirname

from flask import Flask, render_template, request
from flask_socketio import SocketIO

from backend.game import Game

template_dir = os.path.join(dirname(__file__), 'templates')
static_dir = os.path.join(dirname(__file__), 'static')
app = Flask(__name__, template_folder=template_dir, static_url_path=static_dir)
# socket_io = SocketIO(app)
socket_io = SocketIO(app, message_queue='redis://')

human_playing_template_name = 'human_playing.html'
ai_playing_template_name = 'ai_playing.html'
main_template_name = human_playing_template_name


@app.route('/')
def index():
    return render_template(main_template_name)


@app.route('/train_ai')
def train_ai():
    return render_template(ai_playing_template_name)


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
    return render_template(main_template_name)


@app.route('/show_board', methods=['POST'])
def show_board():
    if request.method == 'POST':
        board = app.game.get_board()
        socket_io.emit('board_display', board.tolist())
    return render_template(main_template_name)


@app.route('/show_empty_board', methods=['POST'])
def show_empty_board():
    if request.method == 'POST':
        empty_board = BoardManager().get_board(1)
        socket_io.emit('board_display', empty_board.tolist())
    return render_template(main_template_name)


@app.route('/can_place_block', methods=['POST'])
def can_place_block():
    if request.method == 'POST':
        if not app.game.is_finish:
            response_json = request.get_json()
            rotation_index = response_json['rotation_index']
            start_column = response_json['start_column']
            block_to_be_placed = app.game.current_shape[rotation_index]
            if app.game.player_place_block(start_column, block_to_be_placed):
                socket_io.emit('board_display', app.game.get_board().tolist())
                next_turn()
    return render_template(main_template_name)


@app.route('/reject_current_block', methods=['POST'])
def reject_current_block():
    next_turn()
    return render_template(main_template_name)


@app.route('/start_game', methods=['POST'])
def start_game():
    if request.method == 'POST':
        current_board_number = app.game.board_number
        app.game = Game(current_board_number)
        next_turn()
    return render_template(main_template_name)


@app.route('/restart_game', methods=['POST'])
def restart_game():
    if request.method == 'POST':
        current_board_number = app.game.board_number
        app.game = Game(current_board_number)
        board = app.game.get_board()
        socket_io.emit('board_display', board.tolist())
        next_turn()
    return render_template(main_template_name)


@app.route('/display_board_1', methods=['POST'])
def display_board_1():
    if request.method == 'POST':
        return display_board_number(1)


@app.route('/display_board_2', methods=['POST'])
def display_board_2():
    if request.method == 'POST':
        return display_board_number(2)


@app.route('/display_board_3', methods=['POST'])
def display_board_3():
    if request.method == 'POST':
        return display_board_number(3)


@app.route('/display_board_4', methods=['POST'])
def display_board_4():
    if request.method == 'POST':
        return display_board_number(4)


def display_board_number(board_number: int):
    app.game = Game(board_number)
    board = app.game.get_board()
    socket_io.emit('board_display', board.tolist())
    next_turn()
    return render_template(main_template_name)


def next_turn():
    turn_dict = app.game.next_turn()
    socket_io.emit('extra_current_stats', app.game.get_extra_current_stats())
    if turn_dict['is_finish']:
        final_score = app.game.calculate_total_score()
        socket_io.emit('finished_game', final_score)
    else:
        if 'new_shape' in turn_dict.keys():
            socket_io.emit('current_shape', turn_dict['new_shape'])
        if 'remaining_shapes' in turn_dict.keys():
            socket_io.emit('remaining_shapes', turn_dict['remaining_shapes'])
        score = app.game.calculate_total_score()
        socket_io.emit('display_score', score)


if __name__ == '__main__':
    app.url_base = 'localhost'
    app.port = 5000
    default_board_number = 1
    app.game = Game(default_board_number)
    message_queue = 'redis://'
    socket_io.run(app, host=app.url_base, port=app.port)
