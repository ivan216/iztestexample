import random
import heapq
import time
import matplotlib.pyplot as plt

outer_repeat = 10  # 外层循环次数(防假死)
repeat = 100000  # 内层循环次数
num = 1  # 玉米个数
basic_time = 3950  # 基准时间 cs
hurts = [0 for _ in range(num*60)]
pertube = basic_time // 17  # 扰动范围, 经验值

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
            hurts.extend([0 for _ in range(60)])
        hurts[ht] += 1

    print(f"{(k+1) / outer_repeat:.0%}")

fin_hurts = hurts[:next( (i+1 for i in range(len(hurts)-1,-1,-1) if hurts[i]!=0 ) )]
x = list(range(len(fin_hurts)))

print(f"time cost: {time.time() - st:.2f} s")
print(f"Repeat = {outer_repeat * repeat} times")
print(f"result = {fin_hurts}")

plt.bar(x,fin_hurts)
plt.show()
