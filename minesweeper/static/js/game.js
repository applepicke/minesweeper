
$(function () {
  var win = false;

  // Reveal all previously revealed elements in the map
  revealMap();

  $('#game tbody tr td').click(function (e) {
    var target = e.target;
    var y = target.parentNode.rowIndex;
    var x = target.cellIndex;
    mark(x, y, $(target));
  });

  // Reveal individual position
  function reveal($cell, num) {
    $cell.removeClass('unclicked');
    $cell.addClass('revealed');

    if (num && num !== 'E') {
      $cell.text(num);
    }

    if (num === 'B') {
      $cell.removeClass('revealed');

      if (win) {
        $cell.addClass('mine-win');
      }
      else {
        $cell.addClass('mine');
      }

    }
  }

  // Ask the server to mark a space as clicked
  function mark(x, y, $cell) {
    // Get out of here if it's already marked
    if (!$cell.hasClass('unclicked')) {
      return;
    }

    $.ajax({
      url: 'mark',
      data: {
        x: x,
        y: y
      },
      success: function (result) {

        // Death
        if (result.status === 'dead') {
          handleDeath(x, y, $cell);
          revealMap(result.map);
        }

        // Win
        if (result.status === 'win') {
          revealMap(result.map);
          handleWin();
        }

        // Cleared with nearby bombs
        if (result.status === 'clear') {
          reveal($cell, result.num_bombs);
        }

        // Cleared with no bombs nearby
        if (result.status === 'superclear') {
          for (var i = 0; i < result.empties.length; i++) {
            var x = result.empties[i][0];
            var y = result.empties[i][1];
            var bombs = result.empties[i][2];
            var $newCell = $('#game tbody tr:eq(' + y + ') td:eq(' + x + ')');

            if (bombs >= 0) {
              reveal($newCell, bombs);
            }

          }
          reveal($cell, result.num_bombs);
        }
      },
      error: function (result) {

      }
    });
  }

  // Handle ending death sequence
  function handleDeath(x, y, $cell) {
    $('#death').removeClass('hidden');
  }

  // Victorious winning sequence
  function handleWin() {
    win = true;
    $('#win').removeClass('hidden');
  }

  // Reveal the map based on a map matrix.
  // If no matrix, reveal open spots
  function revealMap(data) {

    $('#game tbody tr td').each(function () {
      var $this = $(this);
      var val = null;

      // Handle a custom data grid
      if (data) {
        y = this.parentNode.rowIndex;
        x = this.cellIndex;
        val = data[y][x];
      }

      // Reveal default items
      else {
        val = $this.text();
      }

      if (val !== '') {
        reveal($this, val);
      }

      if (val === '0') {
        $this.addClass('empty');
      }
    })
  }
});




