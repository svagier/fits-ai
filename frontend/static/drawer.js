let number_of_columns;
let container_height_for_current_block;     // in px
let field_offset;     // in px
let field_size;     // in px
let tallest_block_height;   // in fields
let widest_block_width;   // in fields
let current_block_with_rotations;
let current_rotation;
let current_block_start_column;
let current_block_width;    // in fields
const socketio = io();

// TODO add getting field_colors to FieldType Enum from backend
let field_colors = new Map()
field_colors.set(0, 'grey')   // EMPTY
field_colors.set(1, '#2B252C')   // TAKEN
field_colors.set(2, '#232744')   // EXTRA_EMPTY     // TODO add getting it from background

function setup() {
  $.post("/game_setup")
  $.post("/show_board")
  $.post("/start_game")
}

socketio.on('game_setup', (setup_data) => {
  number_of_columns = setup_data['number_of_columns']
  field_size = setup_data['field_size']
  field_offset = setup_data['field_offset']
  tallest_block_height = setup_data['tallest_block_height']
  widest_block_width = setup_data['widest_block_width']
  container_height_for_current_block = field_size * tallest_block_height + (tallest_block_height - 1) * field_offset
  current_block_start_column = 0
})

socketio.on('board_display', (board) => {
  $(document).ready(function () {
    drawBoard(board)
  });
})

socketio.on('current_shape', (current_block_rotations) => {
  if (current_block_rotations) {
    current_block_with_rotations = current_block_rotations;
    current_rotation = 0;
    current_block_start_column = 0;
    current_block_width = current_block_with_rotations[current_rotation][0].length
    drawCurrentBlock(current_block_rotations[current_rotation])
  }
  else {
    let canvas = document.getElementById('canvas');
    if (canvas.getContext) {
      let ctx = canvas.getContext('2d');
      clearContainerForCurrentBlock(ctx);
    }
  }
})

socketio.on('remaining_shapes', (list_of_remaining_shapes) => {
  console.log(list_of_remaining_shapes)
  $(document).ready(function () {
    let $all_remaining_shapes_container = $('#allRemainingShapesContainer');
    $all_remaining_shapes_container.empty();
    list_of_remaining_shapes.forEach(function callback(shape, index) {
      let shape_container_id = 'remainingShapeContainer' + index
      $all_remaining_shapes_container.append('<div id="' + (shape_container_id) + '" class="remaining-shape-container"></div>')
      let $shape_container = $('#' + shape_container_id);
      let canvas_id = 'remainingShapeCanvas' + index
      $shape_container.append('<canvas id="' + (canvas_id) + '" width="100" height="100"></canvas>')

      let canvas = document.getElementById(canvas_id);
      if (canvas.getContext) {
        let ctx = canvas.getContext('2d');
        ctx.fillStyle = 'green';
        let row_number = 0
        shape.forEach(row => {
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
    });
  });
})

socketio.on('display_score', (score) => {
  $(document).ready(function () {
    $('#currentScoreDisplay').text(score);
  });
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
  let canvas = document.getElementById('canvas');
  if (canvas.getContext) {
    let ctx = canvas.getContext('2d');
    clearContainerForCurrentBlock(ctx);
    ctx.fillStyle = 'green';
    let row_number = 0
    current_block.forEach(row => {
      let column_number = current_block_start_column
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

function rotateCurrentBlockClockwise() {
  if (current_block_with_rotations) {
    current_rotation += 1;
    if (current_rotation === current_block_with_rotations.length) {
      current_rotation = 0;
    }
    current_block_width = current_block_with_rotations[current_rotation][0].length
    current_block_start_column = 0
    drawCurrentBlock(current_block_with_rotations[current_rotation]);
  }
}

function rotateCurrentBlockCounterclockwise() {
  if (current_block_with_rotations) {
    current_rotation -= 1;
    if (current_rotation === -1) {
      current_rotation = current_block_with_rotations.length - 1;
    }
    current_block_width = current_block_with_rotations[current_rotation][0].length
    current_block_start_column = 0
    drawCurrentBlock(current_block_with_rotations[current_rotation]);
  }
}

function moveCurrentBlockLeft() {
  if (current_block_with_rotations) {
    current_block_start_column -= 1;
    if (current_block_start_column <= -1) {
      current_block_start_column = number_of_columns - current_block_width;
    }
    drawCurrentBlock(current_block_with_rotations[current_rotation]);
  }
}

function moveCurrentBlockRight() {
  if (current_block_with_rotations) {
    current_block_start_column += 1;
    if (current_block_start_column > number_of_columns - current_block_width) {
      current_block_start_column = 0;
    }
    drawCurrentBlock(current_block_with_rotations[current_rotation]);
  }
}

function placeCurrentBlock() {
  let data = {"rotation_index": current_rotation, "start_column": current_block_start_column};
  $.ajax({
      type: 'POST',
      contentType: 'application/json',
      url: '/can_place_block',
      dataType : 'json',
      data : JSON.stringify(data),
      success : function(result) {
        jQuery("#clash").html(result);
      },error : function(result){
         console.log(result);
      }
  });
}

function rejectCurrentBlock() {
  $.post("/reject_current_block")
}

function clearContainerForCurrentBlock(ctx) {
  ctx.clearRect(0, 0, ctx.canvas.width, container_height_for_current_block);
}

function startGame() {
  $.post("/start_game")
}
