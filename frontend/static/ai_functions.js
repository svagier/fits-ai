const ai_socketio = io();

function setup() {
  $.post("/game_setup")
  $.post("/show_empty_board")
}

ai_socketio.on('training_info', (training_data) => {
  $(document).ready(function () {
    $('#extraCurrentStats #epochNumber').text(training_data['epoch']);
    $('#extraCurrentStats #lastReward').text(training_data['last_reward']);
  });
})

ai_socketio.on('extra_current_stats', (extra_current_stats) => {
  $(document).ready(function () {
    $('#extraCurrentStats #turnNumber').text(extra_current_stats.turn_number);
  });
})
