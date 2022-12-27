def board_to_string(board):
    asciiBoard = {'.': '⬜', '♟': '🙎🏼‍♂️', '♜': '🏰', '♞': '🎠', '♝': '🕺', '♚': '🎅🏼', '♛': '🤶🏼', 
                    '♙': '🙎🏿‍♂️', '♖': '🏯', '♘': '🐎', '♗': '💃🏼', '♔': '🎅🏿', '♕': '🤶🏿', '\n': '\n', ' ': ' '}
#♖ ♘ ♗        

    board_string = ""
    board_string = board.unicode(empty_square='.', orientation=False)
    board_output = ""
    squareNum = -1
    for character in board_string:
        if character == ' ':
            continue
        if character == '\n':
            board_output += '\n'
            squareNum *= -1
            continue
        if squareNum == -1 and character == '.':
            board_output += '🟫'
            squareNum *= -1
        else:
            board_output += asciiBoard[character]
            squareNum *= -1

    return board_output

def get_next_turn(turn):
    if turn == "White":
        turn = "Black"
    elif turn == "Black":
        turn = "White"
    return turn

def format_long_move(inputed_move, turn):
    inputed_move[0] = inputed_move[0].lower()
    inputed_move[1] = inputed_move[1].lower()
    if inputed_move[0] == "": return ""
    elif inputed_move[1] == "": return ""

    piece_dict = {"rook": "r", "knight": "n", "bishop": "b", "king": "k", "queen": "q", "pawn": "p"}
    try:
        piece_char = piece_dict[inputed_move[0]]
    except KeyError:
        return ""
    
    if turn:
        piece_char.upper()
    
    move = piece_char + inputed_move[1].replace("\n", "")

    return move
