# game_rules.py
# 定義 Mu Tōrere 的基本規則：棋子、鄰接、合法步、移動後棋盤

EMPTY = 0
BLACK = 1   # 玩家 / 黑棋
WHITE = -1  # 電腦 / 白棋


def opponent(player):
    """回傳對手棋子"""
    return -player


def ring_neighbors(i, ring_n):
    """外圈第 i 格的左右鄰居"""
    return (i - 1) % ring_n, (i + 1) % ring_n


def legal_moves(board, turn, ring_n):
    """
    輸入：
        board: 棋盤 tuple，例如 (1,1,1,1,-1,-1,-1,-1,0)
        turn: 目前輪到誰，BLACK=1 或 WHITE=-1
        ring_n: 外圈格數，例如 8 或 9

    輸出：
        所有合法步 list，例如 [(0,8), (3,8)]
    """
    center = ring_n
    moves = []

    # 外圈棋子可以往相鄰空格移動，也可以符合條件時進中心
    for src in range(ring_n):
        if board[src] != turn:
            continue

        left, right = ring_neighbors(src, ring_n)

        # 外圈 -> 相鄰外圈空格
        if board[left] == EMPTY:
            moves.append((src, left))
        if board[right] == EMPTY:
            moves.append((src, right))

        # 外圈 -> 中心
        # 條件：中心空，而且此棋子左右至少有一顆對手棋
        if board[center] == EMPTY:
            if board[left] == opponent(turn) or board[right] == opponent(turn):
                moves.append((src, center))

    # 中心 -> 任一外圈空格
    if board[center] == turn:
        for dst in range(ring_n):
            if board[dst] == EMPTY:
                moves.append((center, dst))

    return moves


def apply_move(board, move):
    """
    執行移動，回傳新的 board。
    不在這裡換 turn，turn 由 BFS 控制。
    """
    src, dst = move
    new_board = list(board)
    new_board[dst] = new_board[src]
    new_board[src] = EMPTY
    return tuple(new_board)