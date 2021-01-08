    $( document ).ready(function() {
        $.post("/show_board")
    });

    const socketio = io();
    socketio.on('board_display', (board) => {
        console.log(board)
    })

