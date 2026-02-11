from collections import defaultdict

def corn_thrower_win_prob_bfs(m, t, prob_threshold=1e-70):
    """
    使用 BFS + 概率传播计算玉米投手获胜概率。
    
    Args:
        m (int): 僵尸初始血量
        t (int): 僵尸无停滞下吃完所需时间（厘秒）
        prob_threshold (float): 概率低于此值的状态将被忽略（剪枝）

    """

    # 投掷延迟（厘秒）
    FIRST_DELAYS = list(range(1, 301))      # 0.01 ~ 3.00s
    LATER_DELAYS = list(range(286, 301))    # 2.86 ~ 3.00s
    BUTTER_STUN = 400                       # 4.00s = 400 cs
    LEN_FIRST_DELAYS = len(FIRST_DELAYS)
    LEN_LATER_DELAYS = len(LATER_DELAYS)

    # 初始状态: (hp, free_time, stun) -> probability
    # 第一轮：从初始状态出发，使用 FIRST_DELAYS
    current_states = {(m, t, 0): 1.0}
    total_win = 0.0
    total_lose = 0.0
    total_pruned = 0.0
    is_first_round = True
    round_count = 0

    while current_states:
        round_count += 1
        next_states = defaultdict(float)

        # 选择延迟列表
        delays = FIRST_DELAYS if is_first_round else LATER_DELAYS
        delay_count = LEN_FIRST_DELAYS if is_first_round else LEN_LATER_DELAYS

        for (hp, free_time, stun), prob in current_states.items():
            # 边界检查（理论上不会发生，但安全起见）
            if hp <= 0:
                total_win += prob
                continue
            if free_time <= 0:
                total_lose += prob
                continue

            prob_div = prob / delay_count
            prob_butter = prob_div * 0.25
            prob_corn = prob_div * 0.75

            for d in delays:
                # 时间推进 d 厘秒
                # 先消耗 stun
                stun_after = max(0, stun - d)
                free_used = max(0, d - stun)  # 只有当 stun < d 时才有自由时间
                new_free = free_time - free_used

                # 检查僵尸是否在这段时间内吃完
                if new_free <= 0:
                    total_lose += prob_div
                    continue

                # 否则，进行投掷结算
                # 黄油 (25%)
                hp1 = hp - 2
                if hp1 <= 0:
                    total_win += prob_butter
                else:
                    # 状态仍活跃
                    next_states[(hp1, new_free, BUTTER_STUN)] += prob_butter

                # 玉米粒 (75%)
                hp2 = hp - 1
                if hp2 <= 0:
                    total_win += prob_corn
                else:
                    next_states[(hp2, new_free, stun_after)] += prob_corn

        # === 剪枝 ===
        current_states = {}
        pruned_this_round = 0.0
        for state, p in next_states.items():
            if p >= prob_threshold:
                current_states[state] = p
            else:
                pruned_this_round += p

        total_pruned += pruned_this_round
        is_first_round = False

        if round_count % 10 == 0:
            print(f"Round {round_count}: {len(current_states)} states, pruned {pruned_this_round:.2e}")
        
        # 安全退出：防止无限循环（理论上会收敛）
        total_active = sum(current_states.values())
        if total_active < prob_threshold:
            total_pruned += total_active
            print("converged, return results.")
            break
        if round_count > 1000:
            total_pruned += total_active
            print("Warning: exceeded 1000 rounds, breaking.")
            break

    return total_win,total_lose,total_pruned

if __name__ == "__main__":
    case_list = [(28,3900,1e-10),(65,5200,1e-16),(80,2480,1e-20),(150,5000,1e-30),(300,5000,1e-70)]
    test_case = 5
    args = case_list[test_case-1]

    prob_win,prob_lose,prob_pruned = corn_thrower_win_prob_bfs(*args)
    print(f"wins {prob_win:.8e}, loses {prob_lose:.8e}, pruned {prob_pruned:.8e}")
