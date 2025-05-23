import numpy as np
import matplotlib.pyplot as plt
import time

test_n = 1e6  # 测试次数
num_work = 0  # 动曾
num_idle = 4  # 静曾

def fun(n_work:int, n_idle:int, n_test:int):
    n_pl = n_work + n_idle
    gen_time = max(5-n_pl,1) if n_pl > 2 else 4 - n_pl  # 决定产生多少次随机数，减少运算量
    time_scale = 200*(gen_time+1) + 159  # 对应最长时间值+1
    atk_list = np.array([74,102,130,158])  # 曾的4次相对命中时机
    t_list = np.array([15*i for i in range(1,187)]+[2790+15*i-(i+1)*i//2 for i in range(1,15)])
    num = 152  # 记录损失血量的向量长度，植物受伤不会超过604hp
    res = np.zeros(num)
    tmp = 1  # 用于输出进度
    rows = np.arange(n_pl)[:,np.newaxis]
    rows = np.tile(rows, (1,4*(gen_time+1)))  # 下标值，用于 dmg_mat 的赋值

    for i in range(n_test):
        eat = np.random.randint(350,354)  #[350,354)
        dmg_mat = np.zeros((n_pl,time_scale))  # 行代表植物，列代表命中时间点
        t_rand = np.random.randint(1,2896,(n_pl,1))
        t = np.searchsorted(t_list, t_rand) + 1  # n_pl*1 矩阵，每行代表该植物的第一个倒计时1~200
        
        if n_work > 0:  # 动曾处理
            low_bound = np.maximum(186-t[:n_work],0)
            up_bound = 200-t[:n_work] +1
            last_atk = np.random.randint(low_bound,up_bound,(n_work,1)) # n_work*1 矩阵，每行代表上一次攻击触发到当前的时长
            pre_hurt = 4 - np.searchsorted(atk_list,last_atk,side='right')  # last_atk 值小于 atk_list 值的个数代表受伤几次
            dmg_mat[:n_work,0] = pre_hurt # 不关心动曾命中时机，直接将值存到 dmg_mat 首列
        
        itvl_mat = np.random.randint(186,201,(n_pl,gen_time))
        t_mat = np.concatenate([t,itvl_mat],axis=1)
        t = np.cumsum(t_mat,axis=1)  # t 现在是 n_pl*(1+gen_time) 矩阵，每列代表攻击触发时间点
        t_reshape = t[:,:,np.newaxis]
        atk_list_reshape = atk_list[np.newaxis,np.newaxis,:]
        t_res = t_reshape + atk_list_reshape  # 攻击触发时间点+相对命中时机=真正的命中时机
        t_res = t_res.reshape(n_pl,-1)  # n_pl*(4+4*gen_time) 矩阵，每行代表一个植物，每列代表一个命中时机

        dmg_mat[rows,t_res] += 1  # 形成最终记录伤害的矩阵，注:若行有重复元素，使用 np.add.at()

        col_sum = np.sum(dmg_mat, axis=0)
        prefix_sum = np.cumsum(col_sum)
        kg_die = np.searchsorted(prefix_sum,15)  # 死亡时间点
        if kg_die <= eat:
            res[0] += 1
        else:
            idx = (kg_die-eat-1)//4 + 1  # 受伤值对应 res 的下标
            res[idx] += 1
        
        ##输出进度
        if i+1 == round(n_test*(tmp/100)):
            ht_count_aver = np.dot(res[1:], np.ones(num-1)) / (i+1)
            ht_hp_aver = np.dot(res, np.arange(num)*4) / (i+1)
            print(f"process:{100*(i+1)/n_test:.0f}% aver_count:{100*ht_count_aver:.3f}% aver_hp:{ht_hp_aver:.5f}")
            tmp += 1
        
    max_idx = np.nonzero(res)[0][-1]
    return res[:max_idx+1]

start_time = time.time()
res = fun(num_work,num_idle,test_n)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"程序运行时间: {elapsed_time} 秒")

## 画图
s = res.size
x = np.arange(s)
ht_count_aver = np.dot(res[1:], np.ones(s-1)) / test_n
ht_hp_aver = np.dot(res, np.arange(s)*4) / test_n

plt.bar(x,res)
plt.yscale('log')
plt.title(f"mean dmg:{ht_hp_aver:.5f} dmg prob:{100*ht_count_aver:.3f}%")
plt.xlabel('dmg')
plt.ylabel('frequency')
plt.show()

# print(res)
