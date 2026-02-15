from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until,FlowManager

import matplotlib.pyplot as plt
import numpy as np

test_count = 2000
times = np.zeros(3000,dtype=int)

# 2480 cs 三个波峰 2412-2456-2480-2504-2516

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str(f'''
        {test_count} -1
        1-1 2-1 3-1 4-1 5-1
        1....
        1....
        1....
        1....
        1....
        gl gl gl gl gl
        0 0 0 0 0
        1-6 2-6 3-6 4-6 5-6''')
    
    zbx = 751.7 # 751.7
    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['1-1']
        zb = iz_test.ground.zombie(0)
        zb.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1
    
    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['2-1']
        zb = iz_test.ground.zombie(1)
        zb.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['3-1']
        zb = iz_test.ground.zombie(2)
        zb.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['4-1']
        zb = iz_test.ground.zombie(3)
        zb.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['5-1']
        zb = iz_test.ground.zombie(4)
        zb.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    iz_test.start_test(jump_frame=1, speed_rate=1, print_interval=100)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)

fin_time = times[:next( (i+1 for i in range(len(times)-1,-1,-1) if times[i]!=0 ) )]
x = np.arange(len(fin_time))
fin_time = fin_time[next((i for i in range(len(fin_time)) if fin_time[i]!=0)):]
x = x[-len(fin_time):]

values = x[fin_time>0]
counts = fin_time[fin_time>0]
total = 5.0 * test_count
mean = np.sum(values*counts) / total
print("mean: ",mean)

vari = np.sum((values-mean)**2 * counts) / (total -1)
std = np.sqrt(vari)
print("std: ",std)

fin_time = fin_time/total
plt.bar(x,fin_time)
plt.show()
