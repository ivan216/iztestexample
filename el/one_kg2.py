import numpy as np
import matplotlib.pyplot as plt
import time

n_test = int(1e6)  # 测试次数
num_work = 2  # 动曾
num_idle = 2  # 静曾

def fun(n_work:int, n_idle:int, n_test:int):
    n_pl = n_work + n_idle
    gen_time = max(5-n_pl,1) if n_pl > 2 else 4 - n_pl  # 决定产生多少次随机数，减少运算量
    time_scale = 200*(gen_time+1) + 159  # 对应时间长度
    atk_list = np.array([74,102,130,158])  # 曾的4次相对命中时机
    t_list = np.array([15*i for i in range(1,187)]+[2790+15*i-(i+1)*i//2 for i in range(1,15)])  # t的分布律
    num = 152  # 记录损失血量的向量长度，植物受伤不会超过604hp
    res = np.zeros(num).astype(int)  # 记录结果
    tmp = 1  # 用于屏幕输出进度

    rows = np.arange(n_pl)[:,np.newaxis]
    rows = np.tile(rows, (1,4*(gen_time+2)))

    if n_work== 0:
        t_work = np.zeros((0,gen_time+2)).astype(int)
    if n_idle == 0:
        t_idle = np.zeros((0,gen_time+2)).astype(int)

    for i in range(n_test):
        eat = np.random.randint(350,354)  # [350,354) 开始啃食时刻
        t_rand = np.random.randint(1,2896,(n_pl,1))
        t = np.searchsorted(t_list, t_rand) + 1  # (n_pl*1)矩阵，每行代表对应植物的第一个倒计时1~200

        dmg_mat = np.zeros((n_pl,time_scale+200))
        itvl_mat = np.random.randint(186,201,(n_pl,gen_time+1))

        if n_work > 0:
            t_work = np.concatenate([t[:n_work],itvl_mat[:n_work]], axis=1)
        if n_idle > 0:
            t[n_work:] += 200
            t_idle = np.concatenate([np.zeros((n_idle,1)).astype(int),t[n_work:],itvl_mat[n_work:,:gen_time]], axis=1)
        
        t_res = np.concatenate([t_work,t_idle], axis=0)
        t_res = np.cumsum(t_res, axis=1)
        t_res = t_res[:,:,np.newaxis]
        t_res = t_res + atk_list
        t_res = t_res.reshape(n_pl,-1)

        dmg_mat[rows,t_res] += 1
        dmg_mat[:,:201] = 0 # 假定0对应-200cs

        col_sum = np.sum(dmg_mat, axis=0)
        prefix_sum = np.cumsum(col_sum)  # 累加后找第一个 >=15的值在第几列，-200为矿工死亡时刻
        kg_die = np.searchsorted(prefix_sum,15) - 200  # 时间点从-200开始
        if kg_die <= eat:   # 矿工死亡时刻反推出植物受到伤害
            res[0] += 1
        else:
            idx = (kg_die-eat-1)//4 + 1  # 受伤值对应 res 的下标
            res[idx] += 1
        
        ##屏幕输出
        if i+1 >= n_test/100*tmp :
            ht_count_aver = np.dot(res[1:], np.ones(num-1)) / (i+1)  # 平均受伤次数
            ht_hp_aver = np.dot(res[1:], np.arange(1,num)*4) / (i+1)  # 平均受伤值
            print(f"process:{100*(i+1)/n_test:.0f}% aver_count:{100*ht_count_aver:.3f}% aver_hp:{ht_hp_aver:.5f}")
            tmp += 1
        
    max_idx = np.nonzero(res)[0][-1]
    return res[:max_idx+1]  # 去掉无用的0值

start_time = time.time()
res = fun(num_work,num_idle,n_test)
end_time = time.time()
print(f"测试次数: {n_test}, 运行时间: {end_time - start_time:.2f} 秒")
print("受伤情况(从0开始, 间隔4): ",res)

## 画图
s = res.size
x = np.arange(s) * 4
ht_count_aver = np.dot(res[1:], np.ones(s-1)) / n_test
ht_hp_aver = np.dot(res[1:], x[1:]) / n_test

plt.bar(x,res)
plt.yscale('log')
plt.title(f"test count:{n_test} mean dmg:{ht_hp_aver:.5f} dmg prob:{100*ht_count_aver:.3f}%")
plt.xlabel('dmg')
plt.ylabel('frequency')
plt.show()
