from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Game state
board = [""] * 9 #inisialisasi dengan array board
current_player = "X" #player menggunakan X
human_player = "X"
ai_player = "O" #AI player menggunakan O
game_over = False
winner = None
history = []  # Menyimpan steps history untuk backtracking

winning_combinations = [ #array untuk menyimpan combinations board state yang menang.
    [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Horizontal
    [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Vertical
    [0, 4, 8], [2, 4, 6]              # Diagonal
]


def check_winner(board): #function untuk cek winning_combinations yang mana board ini match. 
    for combo in winning_combinations:
        if board[combo[0]] and board[combo[0]] == board[combo[1]] == board[combo[2]]:
            return board[combo[0]]
    return None


def empty_spots(board):
    return [i for i, cell in enumerate(board) if cell == ""]


def minimax(new_board, player): #function untuk minimax algorithm
    winner = check_winner(new_board) #untuk ngecek apakah sudah ada pemenangnya
    if winner == human_player: #ini kalo kita yang menang
        return {"score": -10}
    elif winner == ai_player: #ini kalo AI yang menang
        return {"score": 10}
    elif not empty_spots(new_board): #ini kalo seri dan ke-9 kotak di board sudah penuh
        return {"score": 0}

    moves = [] #penampung (list) untuk nyimpen moves-nya

    for index in empty_spots(new_board): #loop untuk ngelewatin semua tempat yang masih kosong
        move = {"index": index} #nyimpen indesk stepnya 
        new_board[index] = player #ngasih tanda di boardnya

        #rekursif minimax yg ngitung nilai skor dari step tersebut
        if player == ai_player:
            result = minimax(new_board, human_player) #next turn player
            move["score"] = result["score"]
        else:
            result = minimax(new_board, ai_player) #next turn AI
            move["score"] = result["score"]

        new_board[index] = "" #return board setelah evaluasi langkah (backtrack)
        moves.append(move) #simpan result step ke daftar stepnya

    # cari langkah dengan result/skor  yang terbaik
    if player == ai_player:
        best_move = max(moves, key=lambda x: x["score"]) #ini AI cari step dengan skor tertinggi
    else:
        best_move = min(moves, key=lambda x: x["score"]) #player cari step dengan skor terendah

    return best_move #return langkah terbaik yg ditemukan


@app.route("/")
def index():
    #route utk menangani step yg dilakukan oleh player
    return render_template("index.html")


@app.route("/move", methods=["POST"])
def move():
    #rute utk menangani step yg dilakukan player
    global board, current_player, game_over, winner, history

    #kalo game over, return statusnya 
    if game_over:
        return jsonify({"board": board, "game_over": game_over, "winner": winner})

    #get dari permintaan yg biasanya langkah yg dipilih pemain dan ambil indeks yg dipilih dari data
    data = request.get_json()
    index = data.get("index")

    if board[index] == "": #jika kotak kosong
        history.append(board[:])  # Simpan state sebelum langkah baru
        board[index] = human_player #isi kotak dengan simbol player
        winner = check_winner(board) # cek apakah step ini bikin player menang
        if winner:
            game_over = True #kondisi kalo ada pemenang, game over
            return jsonify({"board": board, "game_over": game_over, "winner": winner})

        # Langkah AI
        ai_choice = minimax(board, ai_player)["index"] # AI memilih best step pake Minimax
        board[ai_choice] = ai_player # ini isi kotak -pake simbol AI
        winner = check_winner(board) # cek apakah AI menang
        if winner:
            game_over = True # kalo AI menang, game over

    #kembalikan keadaan terbaru board game
    return jsonify({"board": board, "game_over": game_over, "winner": winner})


@app.route("/backtrack", methods=["POST"])
def backtrack():#Backtracking untuk kembali ke langkah sebelumnya atau UNDO 
    global board, game_over, winner, history

    if history:# Ngecek langkah langkahnya ada di dalam history
        board = history.pop()# Kembali ke keadaan langkah sebelumnya
        game_over = False # Riset status game over
        winner = None #Riset pemenangnya
    return jsonify({"board": board, "game_over": game_over, "winner": winner})


@app.route("/restart", methods=["POST"])
def restart():#restart untuk mengulang permainan dari awal
    global board, current_player, game_over, winner, history
    board = [""] * 9 #Riset papan permainan dari awal
    game_over = False # Riset status game over
    winner = None #Riset pemenangnya
    history = [] #riset history permainan
    return jsonify({"board": board, "game_over": game_over, "winner": winner})


if _name_ == "_main_":
    app.run(debug=True)