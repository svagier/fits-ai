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
    $('curremt-shape').empty();
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

        let row_number = 0
        shape.forEach(row => {
          let column_number = 0
          row.forEach(field => {
            let block = document.createElement("div");
            block.setAttribute('id', 'currentBlock-r' + row_number.toString() + 'c' + column_number.toString());
            block.classList.add("block");
            if (field === 1) block.classList.add("taken-current-block");
            $("#" + shape_container_id).append(block);
            column_number += 1
          });
          if (column_number < widest_block_width) {
            for (let i = column_number; i < widest_block_width; i++) {
              let empty_block = document.createElement("div");
              empty_block.setAttribute('id', 'currentBlock-r' + row_number.toString() + 'c' + i.toString());
              empty_block.classList.add("block");
              $("#" + shape_container_id).append(empty_block);
            }
          }
          row_number += 1
        });
        while (row_number < tallest_block_height) {
          for (let col_num = 0; col_num < widest_block_width; col_num++) {
            let empty_block = document.createElement("div");
            empty_block.setAttribute('id', 'currentBlock-r' + row_number.toString() + 'c' + col_num.toString());
            empty_block.classList.add("block");
            $("#" + shape_container_id).append(empty_block);
          }
          row_number += 1
        }

      })
    }
  })
})

socketio.on('display_score', (score) => {
  $(document).ready(function () {
    $('#currentScoreDisplay').text(score);
  });
})

socketio.on('finished_game', (final_score) => {
  $(document).ready(function () {
    $("#current-shape").empty()
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
  let plus_blocks = [3, 4, 5]
  $(document).ready(function () {
    $("#board").empty()
    let row_number = 0
    board.forEach(row => {
      let column_number = 0
      row.forEach(field => {
        let block = document.createElement("div");
        block.setAttribute('id', 'r' + row_number.toString() + 'c' + column_number.toString());
        block.classList.add("block");
        if (field === 0) block.classList.add("empty-block");
        else if (field === 1) block.classList.add("taken-block");
        else if (field === 2) block.classList.add("extra-empty-block");
        else if (plus_blocks.includes(field)) {
          block.classList.add("plus-block");
          let plus_text_div = document.createElement("div");
          plus_text_div.classList.add("block-with-text");
          plus_text_div.classList.add("plus-block");
          if (field === 3)
            plus_text_div.textContent += '+1'
          else if (field === 4)
            plus_text_div.textContent += '+2'
          else if (field === 5)
            plus_text_div.textContent += '+3'
          block.append(plus_text_div);
        }
        $("#board").append(block);
        column_number += 1
      });
      row_number += 1
    });
  });
}

function drawCurrentBlock(current_block) {
  $(document).ready(function () {
    $("#current-shape").empty()
    let row_number = 0
    current_block.forEach(row => {
      let column_number = 0
      row.forEach(field => {
        while (column_number < current_block_start_column) {
          let empty_block = document.createElement("div");
          empty_block.setAttribute('id', 'currentBlock-r' + row_number.toString() + 'c' + column_number.toString());
          empty_block.classList.add("block");
          $("#current-shape").append(empty_block);
          column_number += 1
        }
        let block = document.createElement("div");
        block.setAttribute('id', 'currentBlock-r' + row_number.toString() + 'c' + column_number.toString());
        block.classList.add("block");
        if (field === 1) block.classList.add("taken-current-block");
        $("#current-shape").append(block);
        column_number += 1
      });
      if (column_number < number_of_columns) {
        for (let i = column_number; i < number_of_columns; i++) {
          let empty_block = document.createElement("div");
          empty_block.setAttribute('id', 'currentBlock-r' + row_number.toString() + 'c' + i.toString());
          empty_block.classList.add("block");
          $("#current-shape").append(empty_block);
        }
      }
      row_number += 1
    });
    while (row_number < tallest_block_height) {
      for (let col_num = 0; col_num < widest_block_width; col_num++) {
        let empty_block = document.createElement("div");
        empty_block.setAttribute('id', 'currentBlock-r' + row_number.toString() + 'c' + col_num.toString());
        empty_block.classList.add("block");
        $("#current-shape").append(empty_block);
      }
      row_number += 1
    }
  });
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

function restartGame() {
  $.post("/restart_game")
}

function startGame() {
  $.post("/start_game")
}
