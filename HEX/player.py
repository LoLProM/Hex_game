import heapq
import math
from utils import centrality_matrix, centrality_score, count_bridges, count_threats_to_block, dijkstra_path_length, evaluate
from hex_board import HexBoard
import random

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




