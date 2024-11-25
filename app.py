from flask import Flask, render_template, request, jsonify
import math

app = Flask(__name__)

# Constants
PLAYER_X = 'X'  # AI player
PLAYER_O = 'O'  # User
EMPTY = ''      # Empty cell

# Function to check winner or draw
def check_winner(board):
    for player in [PLAYER_X, PLAYER_O]:
        # Check rows and columns
        for i in range(3):
            if all([cell == player for cell in board[i]]) or all([board[j][i] == player for j in range(3)]):
                return player
        # Check diagonals
        if (board[0][0] == board[1][1] == board[2][2] == player) or (board[0][2] == board[1][1] == board[2][0] == player):
            return player
    # Check for a draw
    if all(cell != EMPTY for row in board for cell in row):
        return "Draw"
    return None

# Minimax algorithm for AI
def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == PLAYER_X:
        return 1
    elif winner == PLAYER_O:
        return -1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    score = minimax(board, False)
                    board[i][j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    score = minimax(board, True)
                    board[i][j] = EMPTY
                    best_score = min(score, best_score)
        return best_score

# AI finds the best move
def find_best_move(board):
    best_score = -math.inf
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_X
                score = minimax(board, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    board = data['board']
    user_move = data.get('user_move')

    # Process user's move
    if user_move:
        row, col = user_move
        if board[row][col] == EMPTY:
            board[row][col] = PLAYER_O

    # Check if user wins
    winner = check_winner(board)
    if winner:
        return jsonify({'board': board, 'winner': winner})

    # AI's turn
    ai_move = find_best_move(board)
    if ai_move:
        board[ai_move[0]][ai_move[1]] = PLAYER_X

    # Check if AI wins after its move
    winner = check_winner(board)
    return jsonify({'board': board, 'winner': winner})

if __name__ == '__main__':
    app.run(debug=True)
