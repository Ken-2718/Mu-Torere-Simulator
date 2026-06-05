# layouts.py
# 定義所有要分析的初始局面
# 最後一格永遠是中心點

BLACK = 1
WHITE = -1
EMPTY = 0

LAYOUTS = {
    # 8格原始版：外圈 0~7，中心 8
    "8_B4_W4": {
        "ring_n": 8,
        "board": (1, 1, 1, 1, -1, -1, -1, -1, 0),
        "turn": BLACK
    },

    # 9格延伸版：外圈 0~8，中心 9
    "9_B4_W4": {
        "ring_n": 9,
        "board": (1, 1, 1, 1, -1, -1, -1, -1, 0, 0),
        "turn": BLACK
    },

    "9_B4_W22": {
        "ring_n": 9,
        "board": (1, 1, 1, 1, -1, -1, 0, -1, -1, 0),
        "turn": BLACK
    },

    "9_B22_W4": {
        "ring_n": 9,
        "board": (1, 1, 0, 1, 1, -1, -1, -1, -1, 0),
        "turn": BLACK
    },

    "9_B13_W4": {
        "ring_n": 9,
        "board": (1, 0, 1, 1, 1, -1, -1, -1, -1, 0),
        "turn": BLACK
    },

    "9_B4_W13": {
        "ring_n": 9,
        "board": (1, 1, 1, 1, -1, 0, -1, -1, -1, 0),
        "turn": BLACK
    },
}