$(document).ready(function () {
  $.post("/show_board")
});

const socketio = io();
socketio.on('board_display', (data) => {
  let board = data[0]
  let field_size = data[1]
  console.log(board)
  $(document).ready(function () {
    draw_board(board, field_size)
  });
})

// TODO add getting field_colors to Field Enum from backend
let field_colors = new Map()
field_colors.set(0, 'grey')   // EMPTY
field_colors.set(1, 'blue')   // TAKEN
field_colors.set(2, '#232744')   // EXTRA_EMPTY     // TODO add getting it from background

function draw_board(board, field_size, field_offset=2) {
  let canvas = document.getElementById('canvas');
  if (canvas.getContext) {
    let ctx = canvas.getContext('2d');
    let row_number = 0
    board.forEach(row => {
      let column_number = 0
      row.forEach(field => {
        ctx.fillStyle = field_colors.get(field);
        ctx.fillRect(column_number * field_size  + column_number * field_offset, row_number * field_size + row_number * field_offset, field_size, field_size);
        column_number += 1
      });
      row_number += 1
    });
  }
}
