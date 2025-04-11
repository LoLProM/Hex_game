from collections import deque
import heapq
import math



adj = [(0,1),(0,-1),(1,-1),(1,0),(-1,1),(-1,0)]


def bfs(g, player_id, size):
    visited = set()
    p = {}
    queue = deque()

    # Inicializar la cola con los nodos iniciales del jugador
    for u in g:
        if player_id == 1 and u[1] == 0:
            queue.append(u)
            visited.add(u)
            p[(u[0], u[1])] = None
        if player_id == 2 and u[0] == 0:
            queue.append(u)
            visited.add(u)
            p[(u[0], u[1])] = None

    # Realizar BFS
    while queue:
        u = queue.popleft()
        for dir in adj:
            v = (u[0] + dir[0], u[1] + dir[1])
            if v not in g:
                continue
            if player_id == 1 and v[1] == size - 1:
                p[v] = u
                return True
            if player_id == 2 and v[0] == size - 1:
                p[v] = u
                return True
            if v not in visited:
                visited.add(v)
                queue.append(v)
                p[v] = u

    return False

import heapq

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


    


    # block_penalty = count_threats_to_block(board, player, size) * 5
    