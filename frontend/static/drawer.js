let container_height_for_current_block;
let field_offset;
let field_size;
let tallest_block_height;
let current_block_with_rotations;
let current_rotation;
const socketio = io();

// TODO add getting field_colors to Field Enum from backend
let field_colors = new Map()
field_colors.set(0, 'grey')   // EMPTY
field_colors.set(1, 'blue')   // TAKEN
field_colors.set(2, '#232744')   // EXTRA_EMPTY     // TODO add getting it from background

function setup() {
  $.post("/game_setup")
  $.post("/show_board")
  $.post("/start_game")
}

socketio.on('game_setup', (setup_data) => {
  field_size = setup_data['field_size']
  field_offset = setup_data['field_offset']
  tallest_block_height = setup_data['tallest_block_height']
  container_height_for_current_block = field_size * tallest_block_height + (tallest_block_height - 1) * field_offset
})

socketio.on('board_display', (board) => {
  $(document).ready(function () {
    drawBoard(board)
  });
})

socketio.on('current_block', (current_block_rotations) => {
  current_block_with_rotations = current_block_rotations;
  current_rotation = 0;
  drawCurrentBlock(current_block_rotations[current_rotation])
})


function drawBoard(board) {
  let canvas = document.getElementById('canvas');
  if (canvas.getContext) {
    let ctx = canvas.getContext('2d');
    let row_number = 0
    board.forEach(row => {
      let column_number = 0
      row.forEach(field => {
        ctx.fillStyle = field_colors.get(field);
        const x_pos = column_number * field_size  + column_number * field_offset
        const y_pos = container_height_for_current_block + row_number * field_size + row_number * field_offset
        ctx.fillRect(x_pos, y_pos, field_size, field_size);
        column_number += 1
      });
      row_number += 1
    });
  }
}

function drawCurrentBlock(current_block) {
  console.log(current_block)
  let canvas = document.getElementById('canvas');
  if (canvas.getContext) {
    let ctx = canvas.getContext('2d');
    clearContainerForCurrentBlock(ctx);
    ctx.fillStyle = 'green';
    let row_number = 0
    current_block.forEach(row => {
      let column_number = 0
      row.forEach(field => {
        if (field) {
          const x_pos = column_number * field_size  + column_number * field_offset
          const y_pos = row_number * field_size + row_number * field_offset
          ctx.fillRect(x_pos, y_pos, field_size, field_size);
        }
        column_number += 1
      });
      row_number += 1
    });
  }
}

function rotateCurrentBlock() {
  current_rotation += 1;
  if (current_rotation === current_block_with_rotations.length) {
    current_rotation = 0;
  }
  drawCurrentBlock(current_block_with_rotations[current_rotation]);
}

function clearContainerForCurrentBlock(ctx) {
  ctx.clearRect(0, 0, ctx.canvas.width, container_height_for_current_block);
}

function startGame() {
  $.post("/start_game")
}
