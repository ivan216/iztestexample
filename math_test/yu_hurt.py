import random
import heapq
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import nbinom
from plot_qq import plot_qq_nbinom,plot_qq_skewnorm

outer_repeat = 10  # 外层循环次数(防假死)
repeat = 100000  # 内层循环次数
num = 1  # 玉米个数
hurts = np.zeros(num*60,dtype=int)
basic_time = 5000  # 基准时间 cs
plant_full = False

# basic_time = 5000
# plant_full = False

if plant_full:
    pertube = basic_time // 14  # 小扰动
else:
    pertube = basic_time // 5  # 大扰动

print("Sim Start")
st = time.time()

for k in range(outer_repeat):
    for _ in range(repeat):
        ht = 0
        itv = []  # 存储命中时机的最小堆
        for _ in range(num):
            # 初次攻击分布
            rand_result = random.randint(0,299) - random.randint(0,14)
            while rand_result < 0:
                rand_result = random.randint(0,299) - random.randint(0,14)
            # 最早黄油命中为 2+141=143
            heapq.heappush(itv, rand_result + 143)
        
        pertube_time = basic_time + random.randint(-pertube,pertube)  # 用均匀扰动近似正态扰动
        total_time = pertube_time
        butter_until = -1  # 黄油结束时机
        curr = heapq.heappop(itv)  # 当前命中时机
        
        while curr < total_time:
            if random.random() < 0.25:
                ht += 2
                if curr >= butter_until:
                    total_time += 400
                else:
                    total_time += 400 + curr - butter_until
                butter_until = curr + 400
            else:
                ht += 1
            curr = heapq.heappushpop(itv, curr + random.randint(286,300))
        
        # 剩余被投出的投掷物伤害
        while curr - 113 <= total_time:
            if random.random() < 0.25:
                ht += 2
            else:
                ht += 1
            if itv:
                curr = heapq.heappop(itv)
            else:
                break
        
        while ht >= len(hurts):
            hurts = np.append(hurts,np.zeros(60,dtype=int))
        hurts[ht] += 1

    print(f"{(k+1) / outer_repeat:.0%}")

test_count = outer_repeat * repeat
hurts = hurts[:next( (i+1 for i in range(len(hurts)-1,-1,-1) if hurts[i]!=0 ) )]
hurts_prob = hurts / test_count
x = np.arange(len(hurts))

print(f"time cost: {time.time() - st:.2f} s")
print('basic time:',basic_time)
print(f"Repeat = {test_count} times")
# print(f"result = {fin_hurts}")

r,p = plot_qq_nbinom(hurts,ifplot=False)
print("r:",r," p:",p)

wd_count = (basic_time - 71) / 143
r_approx: int = np.around(wd_count / 2.93).astype(int)
mean_approx = wd_count * 4688/3195 *1.25 *143/293
p_approx = r_approx / mean_approx
# var_approx = r_approx*(1-p_approx) / p_approx**2  # 化简后得下式
var_approx = mean_approx * (4688/3195 *1.25 *1.43 - 1)  # 当大于200s时越来越不准确
nb_pmf = nbinom.pmf(x,r_approx,p_approx,loc=round(r_approx))
print('mean_approx:',mean_approx,' var_approx:',var_approx)
print('r_approx:',r_approx, ' p_approx:',p_approx)


plt.figure(figsize=(8,6),dpi=150)
plt.plot(x,nb_pmf,color='r',label='nbin approx',linewidth=1)
plt.bar(x,hurts_prob,label='simulate')
plt.title(f'simulate test count = {test_count}, time={basic_time}cs')
plt.legend()
plt.xlabel('dmg')
plt.ylabel('frequency')
plt.show()
