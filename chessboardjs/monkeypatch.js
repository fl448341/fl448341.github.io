(function() {
    var OriginalChessboard = window.Chessboard;
  
    var allBoards = [];
  
    function PatchedChessboard(elementOrId, config) {
      var board = OriginalChessboard(elementOrId, config);
  
      allBoards.push(board);
      return board;
    }
  
    window.Chessboard = PatchedChessboard;
  
    window.addEventListener('resize', function() {
      for (var i = 0; i < allBoards.length; i++) {
        allBoards[i].resize();
      }
    });
  })();
  