from collections import defaultdict

def corn_thrower_win_prob_bfs(m, t, prob_threshold=1e-70, throw = False):
    """
    使用 BFS + 概率传播计算玉米投手获胜概率。
    
    Args:
        m (int): 僵尸初始血量
        t (int): 僵尸无停滞下吃完所需时间（厘秒）
        prob_threshold (float): 概率低于此值的状态将被忽略（剪枝）
        throw (bool): 是否投掷小鬼
    """

    # 投掷延迟（厘秒）
    FIRST_DELAYS = list(range(1, 301))      # 0.01 ~ 3.00s
    LATER_DELAYS = list(range(286, 301))    # 2.86 ~ 3.00s
    BUTTER_STUN = 400                       # 4.00s = 400 cs
    LEN_FIRST_DELAYS = len(FIRST_DELAYS)
    LEN_LATER_DELAYS = len(LATER_DELAYS)

    t_real = t - 141 # 减去投掷物飞行时间

    # 初始状态: (hp, free_time, stun) -> probability
    current_states = {(m, t_real, 0): 1.0}
    total_win = 0.0
    total_lose = 0.0
    total_pruned = 0.0
    total_throw = 0.0
    is_first_round = True
    round_count = 0
    min_throw_time = (t-134)*0.4125  # 近似巨人最晚投掷对应剩余时间
    hp_half = m//2

    while current_states:
        round_count += 1
        next_states = defaultdict(float)

        # 选择延迟列表
        delays = FIRST_DELAYS if is_first_round else LATER_DELAYS
        delay_count = LEN_FIRST_DELAYS if is_first_round else LEN_LATER_DELAYS

        for (hp, free_time, stun), prob in current_states.items():

            prob_div = prob / delay_count
            prob_butter = prob_div * 0.25
            prob_corn = prob_div * 0.75

            for d in delays:
                # 时间推进 d 厘秒, 先消耗 stun
                temp = stun-d
                if temp > 0:
                    stun_after = temp
                    free_used = 0
                else:
                    stun_after = 0
                    free_used = -temp
                
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
                elif throw and hp1 < hp_half and new_free > min_throw_time:
                    total_throw += prob_butter
                else:
                    # 状态仍活跃
                    next_states[(hp1, new_free, BUTTER_STUN)] += prob_butter

                # 玉米粒 (75%)
                hp2 = hp - 1
                if hp2 <= 0:
                    total_win += prob_corn
                elif throw and hp2 < hp_half and new_free > min_throw_time:
                    total_throw += prob_corn
                else:
                    next_states[(hp2, new_free, stun_after)] += prob_corn

        # === 剪枝 ===
        current_states = {}
        pruned_this_round = 0.0
        current_active = 0.0
        for state, p in next_states.items():
            if p >= prob_threshold:
                current_states[state] = p
                current_active += p
            else:
                pruned_this_round += p

        total_pruned += pruned_this_round
        is_first_round = False

        if round_count % 10 == 0:
            print(f"Round {round_count}: {len(current_states)} states, pruned {pruned_this_round:.2e}")
        
        # 收敛退出
        if current_active < prob_threshold:
            total_pruned += current_active
            print("=== converged, return results. ===")
            print(f"t = {t}, m = {m}")
            break

    return total_win,total_lose,total_pruned,total_throw

if __name__ == "__main__":
    case_list = [(28,3904,1e-10),
                 (65,4196,1e-16),(65,6580,1e-16),
                 (80,2412,1e-20),(80,2516,1e-20),
                 (150,4022,1e-35,True),(150,6424,1e-30,True),
                 (300,4022,1e-75,True),(300,6424,1e-65,True)]
    test_case = 7
    args = case_list[test_case-1]

    prob_win,prob_lose,prob_pruned,prob_throw = corn_thrower_win_prob_bfs(*args)
    print(f"wins {prob_win:.8e}, loses {prob_lose:.8e}, pruned {prob_pruned:.8e}, throw {prob_throw:.8e}")
