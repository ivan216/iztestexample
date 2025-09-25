import random
import heapq
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import nbinom,skewnorm,gamma
from plot_qq import plot_qq_nbinom,plot_qq_skewnorm, plot_qq_gamma


outer_repeat = 100  # 外层循环次数(防假死)
repeat = 100000  # 内层循环次数
num = 1  # 玉米个数
hurts = np.zeros(num*60,dtype=int)

# basic_time = 30000  # 基准时间 cs
# plant_full = True
basic_time = 10000
plant_full = False

if plant_full:
    pertube = basic_time // 14  # 小扰动
    # pertube = basic_time // 20
else:
    # pertube = basic_time // 5  # 大扰动
    pertube = basic_time // 4

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

# r,p = plot_qq_nbinom(hurts)
# print("r:",r," p:",p)
# nb_pmf = nbinom.pmf(x,r,p,loc=round(r))

# ksi, omega, alpha = plot_qq_skewnorm(hurts)
# print("ksi:",ksi," omega:",omega," alpha:",alpha)
# n_pmf = skewnorm.pdf(x, alpha, loc = ksi, scale = omega)

alpha, beta, c = plot_qq_gamma(hurts)
print("alpha:",alpha," beta:",beta," c:",c)
g_pdf = gamma.pdf(x,alpha,scale=1/beta,loc=c)

plt.figure()
plt.bar(x,hurts_prob,label='simulate')
# plt.plot(x,nb_pmf,label='nbinom',linewidth=1,color='r')
# plt.plot(x,n_pmf,label='skewnormal',linewidth=1,color='g')
plt.plot(x,g_pdf,label='gamma',linewidth=1,color='g')

plt.title(f"basic_time={basic_time}")
plt.legend()
plt.show()
