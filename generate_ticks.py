import numpy as np

def generate_nice_ticks(max_value, min_value, min_ticks=10, max_ticks=15):
    """
    max_value > min_value であると仮定し、区間 [min_value, max_value] 内で
    目盛りの個数が min_ticks 以上 max_ticks 未満となるような「nice ticks」
    を候補（1×10ⁿ, 2×10ⁿ, 5×10ⁿ, n=-3,...,5）から生成します。
    
    戻り値:
      ticks: 生成された目盛りの配列
      step: 使用した刻み幅
    """
    if max_value < min_value:
        max_value, min_value = min_value, max_value  # 安全のため入れ替え
    
    diff = max_value - min_value

    # 候補となる刻み幅を作成（n=-3～5, multipliers: 1, 2, 5）
    candidates = []
    for n in range(-3, 6):  # n = -3, -2, …, 5
        for m in [1, 2, 5]:
            candidates.append(m * 10**n)
    candidates = sorted(candidates)
    
    chosen_ticks = None
    chosen_step = None

    # 各候補について、[min_value, max_value] 内に含まれる目盛りの個数を求める
    for step in candidates:
        # min_value以上の最小の目盛り（min_value がすでに候補の倍数なら min_value を含む）
        lower_tick = np.ceil(min_value / step) * step
        # max_value以下の最大の目盛り
        upper_tick = np.floor(max_value / step) * step

        # 範囲内に目盛りが存在しなければスキップ
        if lower_tick > upper_tick:
            continue

        # 目盛りの個数は (upper - lower) / step + 1
        count = int(round((upper_tick - lower_tick) / step)) + 1

        # 目盛りの個数が [min_ticks, max_ticks) なら採用
        if min_ticks <= count < max_ticks:
            chosen_step = step
            # 小さな誤差対策として step/10 を足しておく
            chosen_ticks = np.arange(lower_tick, upper_tick + step/10, step)
            break

    # 条件を満たす候補が見つからない場合は、最も目盛り数が min_ticks に近いものを選ぶ
    if chosen_ticks is None:
        best_diff = float('inf')
        for step in candidates:
            lower_tick = np.ceil(min_value / step) * step
            upper_tick = np.floor(max_value / step) * step
            if lower_tick > upper_tick:
                continue
            count = int(round((upper_tick - lower_tick) / step)) + 1
            diff_count = abs(count - min_ticks)
            if diff_count < best_diff:
                best_diff = diff_count
                chosen_step = step
                chosen_ticks = np.arange(lower_tick, upper_tick + step/10, step)

    return chosen_ticks, chosen_step

# 使用例
max_value = 0  # 上限
min_value = 7  # 下限

ticks, step = generate_nice_ticks(max_value, min_value)
print("生成された目盛り:", ticks)
print("使用した刻み幅:", step)
