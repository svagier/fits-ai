const ai_socketio = io();

ai_socketio.on('training_info', (training_data) => {
  $(document).ready(function () {
    $('#extraCurrentStats #epochNumber').text(training_data['epoch']);
    $('#extraCurrentStats #lastReward').text(training_data['last_reward']);
  });
})
