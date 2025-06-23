import random
import heapq
import time

outer_repeat = 10  # 外层循环次数(防假死)
repeat = 10000  # 内层循环次数
num = 1  # 玉米个数
basic_time = 3950  # 基准时间 cs
sum_time = 0.0
sum_basic = 0.0
pertube = basic_time // 15  # 扰动范围, 经验值

print("Sim Start")
st = time.time()

for k in range(outer_repeat):    
    for _ in range(repeat):
 
        itv = []  # 存储黄油出手时机的最小堆
        for _ in range(num):
            # 初次攻击分布
            rand_result = random.randint(0,299) - random.randint(0,14)
            while rand_result < 0:
                rand_result = random.randint(0,299) - random.randint(0,14)
            
            # 迭代直到黄油时机
            while random.random() > 0.25:
                rand_result += random.randint(286,300)
            # 一次出手对应一次伤害, 最早出手为 2+28=30
            heapq.heappush(itv,rand_result + 30)

        pertube_time = basic_time + random.randint(-pertube,pertube)  # 模拟相对于基准时间的浮动
        total_time = pertube_time
        butter_until = -1  # 黄油结束时机
        butter_curr = heapq.heappop(itv)  # 当前黄油时机
        
        while butter_curr < total_time:
            if butter_curr >= butter_until:
                total_time += 400
            else:
                total_time += 400 + butter_curr - butter_until
            butter_until = butter_curr + 400

            # 迭代直到下一次黄油时机
            rand_result = butter_curr +  random.randint(286,300)
            while random.random() > 0.25:
                rand_result += random.randint(286,300)
            butter_curr = heapq.heappushpop(itv, rand_result)
        
        if butter_curr == total_time:  # 出手同时死亡
            total_time += 400  # 视作再停滞400, 并结束

        sum_time += total_time
        sum_basic += pertube_time

    result = sum_time / sum_basic 
    print(f"{(k+1) / outer_repeat:.0%}  {result:.6f}")

print(f"time cost: {time.time() - st:.2f} s")
print(f"Repeat = {outer_repeat * repeat} times")
print(f"result = {result}")
