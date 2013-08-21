$(function () {

  // Reveal all previously revealed elements in the map
  $('#game tbody tr td').each(function () {
    var $this = $(this);
    var val = $this.text();

    if (val !== '') {
      reveal($this);
    }

    if (val === '0') {
      $this.addClass('empty');
    }

  })


  $('#game tbody tr td').click(function (e) {
    var target = e.target;
    var y = target.parentNode.rowIndex;
    var x = target.cellIndex;
    mark(x, y, $(target));
  });

});

function reveal($cell, num) {
  $cell.removeClass('unclicked');
  $cell.addClass('revealed');

  if (num) {
    $cell.text(num);
  }
}

function mark(x, y, $this) {

  // Get out of here if it's already marked
  if (!$this.hasClass('unclicked')) {
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
        handleDeath(x, y);
      }

      // Cleared with nearby bombs
      if (result.status === 'clear') {
        reveal($this, result.num_bombs);
      }

      // Cleared with no bombs nearby
      if (result.status === 'superclear') {
        for (var i = 0; i < result.empties.length; i++) {
          var x = result.empties[i][0];
          var y = result.empties[i][1];
          var $newThis = $('#game tbody tr:eq(' + y + ') td:eq(' + x + ')');
          mark(x, y, $newThis);
        }
        reveal($this, result.num_bombs);
      }
    },
    error: function (result) {
      console.log(result);
    }
  });
}

function handleDeath(x, y) {

}

