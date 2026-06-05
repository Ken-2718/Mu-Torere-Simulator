# wld_analysis.py
# 使用 Retrograde Analysis 反向分析 W / L / D

from collections import deque


def retrograde_analysis(states, succ, pred):
    """
    W / L / D 定義：
        W：目前輪到的人有必勝法
        L：目前輪到的人必敗
        D：雙方最佳策略下和局 / 循環

    輸出：
        label[state] = "W" / "L" / "D"
        dist[state] = 距離終局的步數，D 為 None
    """
    label = {}
    dist = {}

    remaining_children = {s: len(succ[s]) for s in states}
    queue = deque()

    # 沒有合法步者為 L
    for s in states:
        if len(succ[s]) == 0:
            label[s] = "L"
            dist[s] = 0
            queue.append(s)

    while queue:
        s = queue.popleft()

        # 如果子狀態是 L，前一手可以走到它，所以前一狀態是 W
        if label[s] == "L":
            for p in pred[s]:
                if p not in label:
                    label[p] = "W"
                    dist[p] = dist[s] + 1
                    queue.append(p)

        # 如果子狀態是 W，前一狀態少一個安全選項
        elif label[s] == "W":
            for p in pred[s]:
                if p in label:
                    continue

                remaining_children[p] -= 1

                # 所有後繼都是 W，代表自己必敗
                if remaining_children[p] == 0:
                    label[p] = "L"

                    child_dists = [
                        dist[ch] for ch in succ[p]
                        if ch in dist and dist[ch] is not None
                    ]

                    dist[p] = max(child_dists) + 1 if child_dists else 0
                    queue.append(p)

    # 沒被標記到的就是 D
    for s in states:
        if s not in label:
            label[s] = "D"
            dist[s] = None

    return label, dist