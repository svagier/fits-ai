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

// TODO add getting field_display_data to FieldType Enum from backend
let field_display_data = new Map()
field_display_data.set(0, {'background_color': 'grey', 'text_color': null, 'text': null})   // EMPTY
field_display_data.set(1, {'background_color': '#2B252C', 'text_color': null, 'text': null})   // TAKEN
field_display_data.set(2, {'background_color': '#232744', 'text_color': null, 'text': null})   // EXTRA_EMPTY
field_display_data.set(3, {'background_color': 'whitesmoke', 'text_color': 'black', 'text': '+1'})   // PLUS_1
field_display_data.set(4, {'background_color': 'whitesmoke', 'text_color': 'black', 'text': '+2'})   // PLUS_2
field_display_data.set(5, {'background_color': 'whitesmoke', 'text_color': 'black', 'text': '+3'})   // PLUS_3
field_display_data.set(6, {'background_color': 'black', 'text_color': 'red', 'text': '-5'})   // MINUS_5

// field_display_data.set(7, 'black')   // PAIR_1
// field_display_data.set(8, 'black')   // PAIR_2
// field_display_data.set(9, 'black')   // PAIR_3
// field_display_data.set(10, 'black')   // PAIR_4
// field_display_data.set(11, 'black')   // PAIR_5


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
  $(document).ready(function () {
    let $all_remaining_shapes_container = $('#allRemainingShapesContainer');
    $all_remaining_shapes_container.empty();
    if (list_of_remaining_shapes) {
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
    }
  });
})

socketio.on('display_score', (score) => {
  $(document).ready(function () {
    $('#currentScoreDisplay').text(score);
  });
})

socketio.on('finished_game', (final_score) => {
  $(document).ready(function () {
    let canvas = document.getElementById('canvas');
    if (canvas.getContext) {
      let ctx = canvas.getContext('2d');
      clearContainerForCurrentBlock(ctx);
    }
    current_block_with_rotations = null;
    $('#currentScoreDisplay').text(final_score);
    $('#finalScore').text(final_score);
    $('#finishedGameModal').modal('show')
  });
})

socketio.on('extra_current_stats', (extra_current_stats) => {
  $(document).ready(function () {
    $('#extraCurrentStats #takenFieldsInCurrentShape').text(extra_current_stats.taken_fields_in_current_shape);
    $('#extraCurrentStats #takenFieldsInOtherRemainingShapes').text(extra_current_stats.taken_fields_in_remaining_shapes_without_current);
    $('#extraCurrentStats #allUnreachableEmptyFields').text(extra_current_stats.empty_unreachable_fields);
    $('#extraCurrentStats #allRemainingReachableEmptyFields').text(extra_current_stats.all_empty_reachable_fields);

  });
})


function closeFinishedGameModal() {
   $('#finishedGameModal').modal('toggle');
}

function drawBoard(board) {
  let canvas = document.getElementById('canvas');
  if (canvas.getContext) {
    let ctx = canvas.getContext('2d');
    let row_number = 0
    board.forEach(row => {
      let column_number = 0
      row.forEach(field => {
        ctx.fillStyle = field_display_data.get(field)['background_color'];
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

function restartGame() {
  $.post("/restart_game")
}

function startGame() {
  $.post("/start_game")
}
