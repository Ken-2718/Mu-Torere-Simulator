# export_to_js.py
# 主程式：分析所有版本，輸出 analysis_data.js 給 HTML 使用

import json
from collections import Counter

from layouts import LAYOUTS
from bfs_analysis import build_graph
from wld_analysis import retrograde_analysis
from game_rules import legal_moves, opponent

BLACK = 1
WHITE = -1


def key_to_string(state):
    """
    把 Python state 轉成 HTML 可查詢的字串 key。
    例如：
    ((1,1,1,1,-1,-1,-1,-1,0), 1)
    變成：
    "1,1,1,1,-1,-1,-1,-1,0|1"
    """
    board, turn = state
    return ",".join(map(str, board)) + "|" + str(turn)


def outcome_for_black_player(state, label):
    """
    將 W/L/D 轉換成玩家黑棋視角。

    玩家 = 黑棋 BLACK
    電腦 = 白棋 WHITE

    回傳：
        PlayerWin
        ComputerWin
        Draw
    """
    board, turn = state
    state_label = label[state]

    if state_label == "D":
        return "Draw"

    if turn == BLACK:
        return "PlayerWin" if state_label == "W" else "ComputerWin"

    if turn == WHITE:
        return "ComputerWin" if state_label == "W" else "PlayerWin"


def count_player_view(states, label):
    """
    統計玩家黑棋視角下：
        玩家可強制勝
        電腦可強制勝
        和局
    """
    result_counter = Counter()

    for s in states:
        outcome = outcome_for_black_player(s, label)
        result_counter[outcome] += 1

    return {
        "playerWinStates": result_counter["PlayerWin"],
        "computerWinStates": result_counter["ComputerWin"],
        "drawStates": result_counter["Draw"],
    }


def branch_distribution(states, succ):
    """
    統計每個狀態有幾個合法步。
    例如：
        0步：80個狀態
        1步：480個狀態
    """
    counter = Counter(len(succ[s]) for s in states)
    return {str(k): counter[k] for k in sorted(counter)}


def build_state_labels(states, label):
    """
    輸出每個狀態的 W/L/D。
    給 HTML 右側合法步結果使用。
    """
    return {
        key_to_string(s): label[s]
        for s in states
    }


def build_state_dists(states, dist):
    """
    輸出每個狀態的 dist。
    D 狀態為 None。
    """
    return {
        key_to_string(s): dist[s]
        for s in states
    }


def build_state_outcomes(states, label):
    """
    輸出每個狀態從玩家黑棋視角看的結果。
    """
    return {
        key_to_string(s): outcome_for_black_player(s, label)
        for s in states
    }


def build_move_results(states, succ, label, dist, move_map):
    """
    輸出每個狀態下，每個合法步走完後的結果。

    HTML 右側會用這個顯示：
        0 → 8
        W/L/D：D
        玩家視角：Draw
        dist：None
    """
    move_results = {}

    for s in states:
        s_key = key_to_string(s)
        move_results[s_key] = []

        for next_s in succ[s]:
            move = move_map[(s, next_s)]

            move_results[s_key].append({
                "move": list(move),
                "nextKey": key_to_string(next_s),
                "label": label[next_s],
                "dist": dist[next_s],
                "outcome": outcome_for_black_player(next_s, label),
            })

    return move_results

def count_turn_view(states, label):
    """
    分別統計：
    黑棋回合時 W/L/D 數量
    白棋回合時 W/L/D 數量
    """
    black_counter = Counter()
    white_counter = Counter()

    for s in states:
        board, turn = s

        if turn == BLACK:
            black_counter[label[s]] += 1
        elif turn == WHITE:
            white_counter[label[s]] += 1

    return {
        "blackToMove": {
            "W": black_counter["W"],
            "L": black_counter["L"],
            "D": black_counter["D"],
            "total": sum(black_counter.values())
        },
        "whiteToMove": {
            "W": white_counter["W"],
            "L": white_counter["L"],
            "D": white_counter["D"],
            "total": sum(white_counter.values())
        }
    }


def analyze_one_layout(name, config):
    """
    分析單一版本，例如：
        8_B4_W4
        9_B4_W22
    """
    ring_n = config["ring_n"]
    start_board = config["board"]
    start_turn = config["turn"]
    start_state = (start_board, start_turn)

    # 1. BFS 建立狀態圖
    states, succ, pred, move_map = build_graph(
        start_board=start_board,
        start_turn=start_turn,
        ring_n=ring_n
    )

    # 2. W/L/D 反向分析
    label, dist = retrograde_analysis(states, succ, pred)

    # 3. 基本統計
    terminal_count = sum(1 for s in states if len(succ[s]) == 0)
    total_branch = sum(len(succ[s]) for s in states)
    avg_branching = total_branch / len(states)

    W = sum(1 for s in states if label[s] == "W")
    L = sum(1 for s in states if label[s] == "L")
    D = sum(1 for s in states if label[s] == "D")

    # 4. 黑棋/白棋回合分開統計
    turn_view = count_turn_view(states, label)
    
    # 5. 玩家黑棋視角統計
    player_view = count_player_view(states, label)
    
    # 6. 分支數分布
    branch_dist = branch_distribution(states, succ)

    # 7. summary 給左側分析統計面板
    summary = {
        "ringN": ring_n,
    
        # 完整博弈分析
        "reachable": len(states),
        "terminal": terminal_count,
        "W": W,
        "L": L,
        "D": D,
    
        # 黑棋回合 W/L/D
        "blackToMove": turn_view["blackToMove"],
    
        # 白棋回合 W/L/D
        "whiteToMove": turn_view["whiteToMove"],
    
        # 玩家視角：黑棋=玩家，白棋=電腦
        "playerWinStates": player_view["playerWinStates"],
        "computerWinStates": player_view["computerWinStates"],
        "drawStates": player_view["drawStates"],
    
        # 分支數
        "avgBranching": round(avg_branching, 4),
        "branchDistribution": branch_dist,
    
        # 初始局面
        "initialLabel": label[start_state],
        "initialDist": dist[start_state],
        "initialOutcome": outcome_for_black_player(start_state, label),
    }

    # 8. 詳細資料給 HTML 查表
    state_labels = build_state_labels(states, label)
    state_dists = build_state_dists(states, dist)
    state_outcomes = build_state_outcomes(states, label)
    move_results = build_move_results(states, succ, label, dist, move_map)

    return summary, state_labels, state_dists, state_outcomes, move_results


def main():
    """
    主執行函式。
    執行後會輸出 analysis_data.js
    """
    analysis_data = {}
    state_labels = {}
    state_dists = {}
    state_outcomes = {}
    move_results = {}

    for name, config in LAYOUTS.items():
        print("=" * 60)
        print(f"Analyzing {name} ...")

        summary, labels, dists, outcomes, moves = analyze_one_layout(name, config)

        analysis_data[name] = summary
        state_labels[name] = labels
        state_dists[name] = dists
        state_outcomes[name] = outcomes
        move_results[name] = moves

        print(summary)

    # 輸出成 JavaScript 檔案，讓 HTML 用 <script src="analysis_data.js"></script> 讀取
    js = ""

    js += "const ANALYSIS_DATA = "
    js += json.dumps(analysis_data, ensure_ascii=False, indent=2)
    js += ";\n\n"

    js += "const STATE_LABELS = "
    js += json.dumps(state_labels, ensure_ascii=False, indent=2)
    js += ";\n\n"

    js += "const STATE_DISTS = "
    js += json.dumps(state_dists, ensure_ascii=False, indent=2)
    js += ";\n\n"

    js += "const STATE_OUTCOMES = "
    js += json.dumps(state_outcomes, ensure_ascii=False, indent=2)
    js += ";\n\n"

    js += "const MOVE_RESULTS = "
    js += json.dumps(move_results, ensure_ascii=False, indent=2)
    js += ";\n"

    with open("analysis_data.js", "w", encoding="utf-8") as f:
        f.write(js)

    print("=" * 60)
    print("Done. Exported analysis_data.js")


if __name__ == "__main__":
    main()