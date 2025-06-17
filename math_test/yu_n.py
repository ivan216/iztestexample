import random
import heapq
import time

outer_repeat = 10  # 外层循环次数（防假死）
repeat = 100000  # 内层循环次数
num = 2  # 玉米个数
basic_time = 3900  # 基准时间 cs
sum_time = 0.0
sum_basic = 0.0
print("Sim Start")
st = time.time()

for k in range(outer_repeat):    
    
    for i in range(repeat):
        pertube_time = basic_time + random.randint(-200,200)  # 模拟相对于基准时间的浮动
        # 录入第一次玉米攻击时机
        itv = []
        for _ in range(num):
            rand_result = random.randint(0,299) - random.randint(0,14)
            while rand_result < 0:
                rand_result = random.randint(0,299) - random.randint(0,14)
            heapq.heappush(itv,rand_result)

        total_time = pertube_time
        butter_until = -1
        curr = heapq.heappop(itv)
        
        while curr <= total_time:
            if random.random() <= 0.25:
                if curr >= butter_until:
                    total_time += 400
                else:
                    total_time += 400 + curr - butter_until
                butter_until = curr + 400

            curr = heapq.heappushpop(itv, curr + random.randint(286, 300))

        sum_time += total_time
        sum_basic += pertube_time

    result = sum_time / sum_basic 
    print(f"{(k+1) / outer_repeat:.0%}  {result:.6f}")

print(f"time cost: {time.time() - st:.2f} s")
print(f"Repeat = {outer_repeat * repeat} times")
print(f"Avg = {result}")
