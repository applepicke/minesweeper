$(function () {

  // Click handlers
  $('#new-game').click(function (e) {
    var name = $('#new-game-name').val().trim();

    if (!checkName(name)) {
      return;
    }

    $.ajax({
      url: '/create_game',
      data: { name: name },
      success: function (result) {
        if (result === 'game-created') {
          window.location.replace('/games/' + name);
        }
      },
      error: function (result) {
        if (result.responseText === 'game-exists') {
          $('#errors').text('Game already exists.');
        }
        if (result.responseText === 'no-fancy-names') {
          $('#errors').text('No fancy characters allowed in your name!');
        }

      }
    });


  });

  $('#continue-game').click(function (e) {
    var name = $('#new-game-name').val().trim();

    if (!checkName(name)) {
      return;
    }

    $.ajax({
      url: '/check_game',
      data: { name: name },
      success: function (result) {
        if (result === 'game-exists') {
          window.location.replace('/games/' + name);
        }
      },
      error: function (result) {
        if (result.responseText === 'game-doesnt-exist') {
          $('#errors').text('Game doesn\'t exist.');
        }
      }
    });

  });

});

function checkName(name) {
  if (name === '') {
    $('#errors').text('Must specify a game name.');
    return false;
  }
  return true;
}