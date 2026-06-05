# bfs_analysis.py
# 使用 BFS 從初始局面出發，建立完整可達狀態圖

from collections import deque, defaultdict
from game_rules import legal_moves, apply_move, opponent


def build_graph(start_board, start_turn, ring_n):
    """
    輸入：
        start_board: 初始棋盤
        start_turn: 初始回合
        ring_n: 外圈格數

    輸出：
        states: 所有可達狀態
        succ: 每個狀態的後繼狀態
        pred: 每個狀態的前驅狀態
        move_map: (state, next_state) 對應是哪一步 move
    """
    start_state = (start_board, start_turn)

    states = set([start_state])
    queue = deque([start_state])

    succ = defaultdict(list)
    pred = defaultdict(list)
    move_map = {}

    while queue:
        board, turn = queue.popleft()
        state = (board, turn)

        moves = legal_moves(board, turn, ring_n)

        for move in moves:
            next_board = apply_move(board, move)
            next_turn = opponent(turn)
            next_state = (next_board, next_turn)

            succ[state].append(next_state)
            pred[next_state].append(state)
            move_map[(state, next_state)] = move

            if next_state not in states:
                states.add(next_state)
                queue.append(next_state)

    # 確保 terminal state 也有空 succ / pred
    for s in states:
        succ[s] = succ.get(s, [])
        pred[s] = pred.get(s, [])

    return states, succ, pred, move_map