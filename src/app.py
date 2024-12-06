from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Game state
board = [""] * 9
current_player = "X"
human_player = "X"
ai_player = "O"
game_over = False
winner = None
history = []  # Menyimpan riwayat langkah-langkah

winning_combinations = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
    [0, 4, 8], [2, 4, 6]              # Diagonal
]


def check_winner(board):
    for combo in winning_combinations:
        if board[combo[0]] and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]
    return None


def empty_spots(board):
    return [i for i, cell in enumerate(board) if cell == ""]


def minimax(new_board, player):
    winner = check_winner(new_board)
    if winner == human_player:
        return {"score": -10}
    elif winner == ai_player:
        return {"score": 10}
    elif not empty_spots(new_board):
        return {"score": 0}

    moves = []

    for index in empty_spots(new_board):
        move = {"index": index}
        new_board[index] = player

        if player == ai_player:
            result = minimax(new_board, human_player)
            move["score"] = result["score"]
        else:
            result = minimax(new_board, ai_player)
            move["score"] = result["score"]

        new_board[index] = ""
        moves.append(move)

    if player == ai_player:
        best_move = max(moves, key=lambda x: x["score"])
    else:
        best_move = min(moves, key=lambda x: x["score"])

    return best_move


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    global board, current_player, game_over, winner, history

    if game_over:
        return jsonify({"board": board, "game_over": game_over, "winner": winner})

    data = request.get_json()
    index = data.get("index")

    if board[index] == "":
        history.append(board[:])  # Simpan state sebelum langkah baru
        board[index] = human_player
        winner = check_winner(board)
        if winner:
            game_over = True
            return jsonify({"board": board, "game_over": game_over, "winner": winner})

        # Langkah AI
        ai_choice = minimax(board, ai_player)["index"]
        board[ai_choice] = ai_player
        winner = check_winner(board)
        if winner:
            game_over = True

    return jsonify({"board": board, "game_over": game_over, "winner": winner})


@app.route("/backtrack", methods=["POST"])
def backtrack():
    global board, game_over, winner, history

    if history:
        board = history.pop()
        game_over = False
        winner = None
    return jsonify({"board": board, "game_over": game_over, "winner": winner})


@app.route("/restart", methods=["POST"])
def restart():
    global board, current_player, game_over, winner, history
    board = [""] * 9
    game_over = False
    winner = None
    history = []
    return jsonify({"board": board, "game_over": game_over, "winner": winner})


if __name__ == "__main__":
    app.run(debug=True)