import math
from collections import defaultdict

# 实际上不用log结果无区别，浮点数精度足够

def logsumexp(log_probs):
    """安全计算多个对数概率的和"""
    if not log_probs:
        return -math.inf
    max_log = max(log_probs)
    # 避免除以零，使用 exp(lp - max_log) 防止溢出
    return max_log + math.log(sum(math.exp(lp - max_log) for lp in log_probs))

def corn_thrower_win_prob_bfs_log(m, t, prob_threshold=1e-70):
    """
    使用对数域 BFS + 概率传播计算玉米投手获胜概率。
    
    Args:
        m (int): 僵尸初始血量
        t (int): 僵尸无停滞下吃完所需时间（厘秒）
        prob_threshold (float): 普通概率阈值（用于剪枝）
    
    Returns:
        tuple: (win_probability, total_pruned_probability_mass)
    """
    
    # 常量定义
    FIRST_DELAYS = list(range(1, 301))      # 1~300 cs
    LATER_DELAYS = list(range(286, 301))    # 286~300 cs
    BUTTER_STUN = 400                       # 4.00s = 400 cs
    
    # 预计算对数常量
    LOG_DELAY_FIRST = math.log(len(FIRST_DELAYS))  # log(300)
    LOG_DELAY_LATER = math.log(len(LATER_DELAYS))  # log(15)
    LOG_BUTTER = math.log(0.25)                   # log(0.25)
    LOG_CORN = math.log(0.75)                     # log(0.75)
    
    # 转换概率阈值为对数形式
    log_threshold = math.log(prob_threshold) if prob_threshold > 0 else -math.inf
    
    # 初始状态: (hp, free_time, stun) -> log_prob
    current_states = {(m, t, 0): 0.0}  # log(1.0) = 0.0
    total_win_log = -math.inf
    total_lose_log = -math.inf
    total_pruned = 0.0
    is_first_round = True
    round_count = 0

    while current_states:
        round_count += 1
        next_states = defaultdict(list)  # 状态 -> [log_prob1, log_prob2, ...]

        for (hp, free_time, stun), log_prob in current_states.items():
            # 边界检查（已结束状态不应在current_states中，但安全检查）
            if hp <= 0:
                # 累加到总胜率（转换为普通概率）
                total_win_log = logsumexp([total_win_log, log_prob])
                continue
            if free_time <= 0:
                total_lose_log = logsumexp([total_lose_log, log_prob])
                continue

            # 选择延迟分布
            delays = FIRST_DELAYS if is_first_round else LATER_DELAYS
            log_delay = LOG_DELAY_FIRST if is_first_round else LOG_DELAY_LATER

            for d in delays:
                # 时间推进
                stun_after = max(0, stun - d)
                free_used = max(0, d - stun)
                new_free = free_time - free_used

                # 检查僵尸是否吃完
                if new_free <= 0:
                    # 累加到失败概率
                    total_lose_log = logsumexp([total_lose_log, log_prob - log_delay])
                    continue

                # 黄油攻击 (25%)
                hp1 = hp - 2
                if hp1 <= 0:
                    # 直接累加到胜率
                    total_win_log = logsumexp([total_win_log, log_prob - log_delay + LOG_BUTTER])
                else:
                    # 添加到下一状态
                    next_states[(hp1, new_free, BUTTER_STUN)].append(log_prob - log_delay + LOG_BUTTER)

                # 玉米粒攻击 (75%)
                hp2 = hp - 1
                if hp2 <= 0:
                    total_win_log = logsumexp([total_win_log, log_prob - log_delay + LOG_CORN])
                else:
                    next_states[(hp2, new_free, stun_after)].append(log_prob - log_delay + LOG_CORN)

        # === 合并下一状态并剪枝 ===
        current_states = {}
        pruned_this_round = 0.0
        for state, log_probs in next_states.items():
            # 合并多个路径
            total_log = logsumexp(log_probs)
            
            # 检查是否超过阈值
            if total_log > log_threshold:
                current_states[state] = total_log
            else:
                pruned_this_round += math.exp(total_log)  # 转换为普通概率

        total_pruned += pruned_this_round
        is_first_round = False

        if round_count % 10 == 0:
            print(f"Round {round_count}: {len(current_states)} states, pruned {pruned_this_round:.2e}")

        # 安全退出：概率质量已极低
        total_active = sum(math.exp(log_prob) for log_prob in current_states.values())
        if total_active <= prob_threshold:
            # 将剩余活跃概率计入剪枝
            total_pruned += total_active
            current_states.clear()
            print("converged, return results")
            break
        if round_count > 1000:
            total_pruned += total_active
            current_states.clear()
            print("Warning: exceeded 1000 rounds, breaking.")
            break

    # 转换最终结果为普通概率
    win_prob = math.exp(total_win_log) if total_win_log > -math.inf else 0.0
    lose_prob = math.exp(total_lose_log) if total_lose_log > -math.inf else 0.0
    return win_prob, lose_prob, total_pruned

if __name__ == "__main__":
    case_list = [(28,3900,1e-10),(65,5200,1e-16),(80,2480,1e-20),(150,5000,1e-30),(300,5000,1e-70)]
    test_case = 5
    args = case_list[test_case-1]

    prob_win,prob_lose,prob_pruned = corn_thrower_win_prob_bfs_log(*args)
    print(f"wins {prob_win:.8e}, loses {prob_lose:.8e}, pruned {prob_pruned:.8e}")
