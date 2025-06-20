import numpy as np
import matplotlib.pyplot as plt
import time
import multiprocessing

num = 152  # 记录损失血量的向量长度, 植物受伤不会超过604hp
atk_list = np.array([74, 102, 130, 158])  # 曾的4次相对命中时刻
t_list = np.array([15*i for i in range(187)] + [2790 + 15*i - (i+1)*i//2 for i in range(1,15)])  # t的分布律

def fun(n_work: int, n_idle: int, n_test_sub: int):
    res = np.zeros(num, dtype=int)
    n_pl = n_work + n_idle
    gen_time = max(5 - n_pl, 1) if n_pl > 2 else 4 - n_pl  # 决定产生多少次随机数
    if n_work > 0:
        gen_time += 1  # 动曾gen_time多1次
    time_scale = 200 * (gen_time + 1) + 159  # 对应时间段的总长度(包括端点)
    rows = np.arange(n_pl)[:, np.newaxis]
    rows = np.tile(rows, (1, 4*(gen_time + 1)))  # 下标值, 用于dmg_mat的赋值
    zero_arr = np.zeros((n_idle, 1), dtype=int)  # 避免在循环体中重复生成0向量
    eat_values = np.random.randint(350, 354, size=n_test_sub) 
    t_rand_values = np.random.randint(2895, size=(n_test_sub, n_pl, 1))
    itvl_mat_big = np.random.randint(186, 201, (n_test_sub, n_pl, gen_time))

    for i in range(n_test_sub):
        eat = eat_values[i]  # [350,354)开始啃食时刻
        t_rand = t_rand_values[i]
        itvl_mat = itvl_mat_big[i]  # 每个植物每次重置的随机数形成的矩阵
        t = np.searchsorted(t_list, t_rand, side='right')  # (n_pl*1)矩阵, 每行代表对应植物的第一个倒计时1~200
        dmg_mat = np.zeros((n_pl, time_scale), dtype=int)  # 命中时机矩阵, 行代表植物, 列代表时机(从-200cs/0cs开始)
        
        if n_work == 0 or n_idle == 0:  # 只有动曾或只有静曾
            t_res = np.concatenate([t, itvl_mat], axis=1)  # 将t与随机数矩阵合并
        else:
            t_work = np.concatenate([t[:n_work], itvl_mat[:n_work]], axis=1)  # 动曾对应矩阵
            t_idle = np.concatenate([zero_arr, t[n_work:] + 200, itvl_mat[n_work:, :-1]], axis=1)
            # 静曾对应矩阵, 用0向量填充使得与动曾维度一致, 0向量的影响可以在后面消去
            # 静曾真正开始时间是0cs, 要将t[n_work:]值增加200, 根据初次攻击分布, 这种处理是合理的
            t_res = np.concatenate([t_work, t_idle], axis=0)  # 动静曾合并为大矩阵一起处理

        t_res = np.cumsum(t_res, axis=1)  # 累加得到每个攻击触发时间点
        t_res = t_res[:, :, np.newaxis] + atk_list  # 增加维度来与atk_list广播加和, 攻击触发时刻 + 相对命中时刻 = 真正的命中时刻
        t_res = t_res.reshape(n_pl, -1)  # n_pl*(4+4*gen_time)矩阵, 行代表植物, 列代表命中时刻(还可能有一些由0向量带来的假值)

        dmg_mat[rows, t_res] = 1  # 对dmg_mat相应元素赋值
        if n_work > 0:  # 含动曾要特殊处理, -200~0cs全部删去, 0向量带来影响也同时被删去
            dmg_mat = dmg_mat[:, 201:]
        col_sum = np.sum(dmg_mat, axis=0)
        prefix_sum = np.cumsum(col_sum)  # 累加后的值代表伤害
        kg_die = np.searchsorted(prefix_sum, 15)
        if n_work > 0:  # 含动曾要特殊处理, 原本的0cs被删去, 因此+1才是真正时刻
            kg_die += 1

        if kg_die <= eat:  # 由矿工死亡时刻可以反推出植物受到伤害
            res[0] += 1
        else:
            idx = (kg_die - eat - 1) // 4 + 1  # 受伤值对应res的下标
            res[idx] += 1
    return res

def multi_process_fun(n_work: int, n_idle: int, n_test: int, num_processes):
    n_test_sub = n_test // num_processes
    remainder = n_test % num_processes

    with multiprocessing.Pool(processes=num_processes) as pool:
        first_process_n_test = n_test_sub + remainder
        results = [pool.apply_async(fun, args=(n_work, n_idle, first_process_n_test))]
        for _ in range(1, num_processes):
            results.append(pool.apply_async(fun, args=(n_work, n_idle, n_test_sub)))
        
        res = np.zeros(num,dtype=int)
        for result in results:
            sub_res = result.get()
            res += sub_res
    return res

if __name__ == "__main__":
    outer_repeat = 10  # 外层循环次数
    n_test_per_loop = 10**6  # 内层循环的测试次数
    num_work = 0  # 动曾数量
    num_idle = 4  # 静曾数量
    num_processes = multiprocessing.cpu_count()  # 使用所有可用的CPU核心
    
    print(f"开始{outer_repeat}次外层循环测试，每次循环{n_test_per_loop:,}次模拟...")
    start_time = time.time()
    # 初始化累计结果
    cumulative_res = np.zeros(num,dtype=int)
    cumulative_tests = 0
    cum_x = np.arange(num) * 4

    for i in range(outer_repeat):
        res = multi_process_fun(num_work, num_idle, n_test_per_loop, num_processes)
        # 累加结果
        cumulative_res += res
        cumulative_tests += n_test_per_loop
        cum_count_aver = cumulative_res[1:].sum() / cumulative_tests
        cum_hp_aver = np.dot(cumulative_res[1:], cum_x[1:].astype(float)) / cumulative_tests
        # 输出累计结果
        print(f"循环 {i+1}/{outer_repeat}: 累计次数={cumulative_tests:,} | 平均伤害={cum_hp_aver:.6f} | 平均次数={cum_count_aver:.4%}")

    end_time = time.time()
    
    # 最终结果计算
    max_idx = np.nonzero(res)[0][-1] if np.count_nonzero(res) > 0 else 0
    final_res = cumulative_res[:max_idx+1]  # 清除尾部零元素
    x = np.arange(max_idx+1) * 4
    
    print(f"\n===== 全部{outer_repeat}次循环完成 =====")
    print(f"总测试次数: {cumulative_tests:,}")
    print(f"总运行时间: {end_time-start_time:.2f}秒")
    print(f"最终结果: 平均伤害={cum_hp_aver:.6f} | 平均次数={cum_count_aver:.4%}")
    print("受伤情况(从0开始, 间隔4):", final_res)

    # 绘制最终结果图
    plt.figure(figsize=(10, 6))
    plt.bar(x, final_res, color='skyblue')
    plt.yscale('log')
    plt.title(f"test num:{cumulative_tests:,} dmg:{cum_hp_aver:.6f} dmg prob:{cum_count_aver:.4%}")
    plt.xlabel('dmg')
    plt.ylabel('frequency')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
