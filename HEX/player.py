import heapq
import math
from hex_board import HexBoard
import random
import heapq

# Definición de la clase base Player
# Esta clase representa un jugador en el juego Hex.

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # 1 (rojo) or 2 (azul)

    def play(self, board: "HexBoard") -> tuple:
        raise NotImplementedError("Implement this method!")
    
# Este es el que tenemos que hacer nosotros
class IAPlayer(Player):
    def __init__(self, player_id: int):
        super().__init__(player_id)

    def play(self, board: HexBoard) -> tuple:
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        for move in random.sample(board.get_possible_moves(), len(board.get_possible_moves())):
            board.place_piece(move[0], move[1], self.player_id)
            if board.check_connection(self.player_id):
                board.board[move[0]][move[1]] = 0
                return move
            score = self.minimax(board, depth = 3 if len(board.get_possible_moves()) <= 36 else 1, alpha = alpha, beta = float('inf'), current_id = 3 -self.player_id)
            board.board[move[0]][move[1]] = 0
            if score > best_score:
                best_score = score
                best_move = move
                alpha = max(alpha, score)
        return best_move
    

    def minimax(self, board: HexBoard, depth: int, alpha: int, beta: int, current_id: int):
        
        oponent_id = 3 - self.player_id
        
        if depth == 0 :
            return evaluate(board.board, self.player_id, board.size)
            
        if len(board.get_possible_moves()) == 0:
            return 0
        
        if current_id == self.player_id:
            max_eval = float('-inf')
            for move in self.get_sorted_moves(board, current_id):
                board.place_piece(move[0], move[1],current_id)
                current_eval = self.minimax(board, depth - 1,alpha, beta,oponent_id)
                board.board[move[0]][move[1]] = 0
                current_eval = max(max_eval,current_eval)
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
            return max_eval
        
        if current_id == oponent_id:
            min_eval = float('inf')
            for move in self.get_sorted_moves(board, current_id):
                board.place_piece(move[0], move[1], current_id)
                current_eval = self.minimax(board, depth - 1,alpha, beta, oponent_id)
                board.board[move[0]][move[1]] = 0
                current_eval = min(min_eval,current_eval)
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
            return min_eval
        
    def get_sorted_moves(self, board: HexBoard, player_id: int) -> list:
        moves = board.get_possible_moves()
        scored_moves = []

        for move in moves:
            x, y = move
            board.place_piece(x, y, player_id)
            score = evaluate(board.board, self.player_id, board.size)
            board.board[x][y] = 0
            scored_moves.append((score, move))

        scored_moves.sort(reverse=True)
        return [move for score, move in scored_moves]




# --- Utilidades del tablero ---
def get_neighbors(x, y, size):
    directions = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0)]
    return [
        (nx, ny)
        for dx, dy in directions
        if 0 <= (nx := x + dx) < size and 0 <= (ny := y + dy) < size
    ]

# --- Heurística de camino más corto (Dijkstra) ---
def dijkstra_path_length(board, player, size):

    dist = [[float('inf')] * size for _ in range(size)]
    heap = []

    if player == 1:  # conecta de izquierda a derecha
        for x in range(size):
            if board[x][0] != 3 - player:
                dist[x][0] = 0 if board[x][0] == player else 1
                heapq.heappush(heap, (dist[x][0], x, 0))
    else:  # conecta de arriba a abajo
        for y in range(size):
            if board[0][y] != 3 - player:
                dist[0][y] = 0 if board[0][y] == player else 1
                heapq.heappush(heap, (dist[0][y], 0, y))

    while heap:
        d, x, y = heapq.heappop(heap)
        for nx, ny in get_neighbors(x, y, size):
            if board[nx][ny] == 3 - player:
                continue
            cost = 0 if board[nx][ny] == player else 1
            if dist[nx][ny] > dist[x][y] + cost:
                dist[nx][ny] = dist[x][y] + cost
                heapq.heappush(heap, (dist[nx][ny], nx, ny))

    if player == 1:
        return min(dist[x][size-1] for x in range(size))
    else:
        return min(dist[size-1][y] for y in range(size))

# --- Centralidad ---
def centrality_matrix(size):
    mid = size // 2
    return [[-abs(x - mid) - abs(y - mid) for y in range(size)] for x in range(size)]

def centrality_score(board, player, weights):
    return sum(
        weights[x][y]
        for x in range(len(board))
        for y in range(len(board))
        if board[x][y] == player
    )

# --- Bridges ---
def count_bridges(board, player):
    size = len(board)
    bridges = 0
    directions = [(-1, 1), (1, -1), (-1, -1), (1, 1)]
    for x in range(size):
        for y in range(size):
            if board[x][y] != player:
                continue
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                mx, my = x + dx // 2, y + dy // 2
                if (0 <= nx < size and 0 <= ny < size and
                    board[nx][ny] == player and
                    0 <= mx < size and 0 <= my < size and
                    board[mx][my] == 0):
                    bridges += 1
    return bridges

# --- Amenazas del oponente ---
def count_threats_to_block(board, player, size,threshold=2):
    opponent = 3 - player
    threats = 0
    base_path = dijkstra_path_length(board, opponent, size)

    for x in range(size):
        for y in range(size):
            if board[x][y] != 0:
                continue
            board[x][y] = opponent
            new_path = dijkstra_path_length(board, opponent,size)
            board[x][y] = 0

            if base_path - new_path >= threshold:
                threats += 1
    return threats

# --- Heurística completa ---
def evaluate(board, player, size):
    opponent = 3 - player

    my_path = dijkstra_path_length(board, player,size)
    opp_path = dijkstra_path_length(board, opponent,size)
    path_score = (opp_path - my_path) * 10
    # Combina distancia y conexiones con pesos
    central_weights = centrality_matrix(size)
    central_score = centrality_score(board, player, central_weights)

    bridge_score = count_bridges(board, player) 
    bridge_score_oponent = count_bridges(board, opponent)
    bridge_total = bridge_score_oponent - bridge_score 
    
    return  path_score + (central_score) + (bridge_total)


    