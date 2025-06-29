from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until,FlowManager
from rpze.iztest.operations import place
from rpze.structs.zombie import ZombieType
import matplotlib.pyplot as plt
import numpy as np

test_count = 10000
times = np.zeros(10000,dtype=int)

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str(f'''
        {test_count//5} -1
        1-1 2-1 3-1 4-1 5-1
        1....
        1....
        1....
        1....
        1....
        xg
        0
        1-6''')
    
    #  起始 x = 818.0, x < 121 举锤, +134 cs 砸扁
    #  5000cs
    zbx = 818.0
    end1 = end2 = end3 = end4 = end5 = False
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        zb = iz_test.ground.zombie(0)
        zb.die_no_loot()
    
    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        nonlocal end1
        zb = iz_test.game_board.iz_place_zombie(0,8,ZombieType.gargantuar)
        zb.x = zbx
        await until(lambda _:zb.x < 121).after(134)
        end_time = fm.time
        end1 = True
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1
    
    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        nonlocal end2
        zb = iz_test.game_board.iz_place_zombie(1,8,ZombieType.gargantuar)
        zb.x = zbx
        await until(lambda _:zb.x < 121).after(134)
        end_time = fm.time
        end2 = True
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        nonlocal end3
        zb = iz_test.game_board.iz_place_zombie(2,8,ZombieType.gargantuar)
        zb.x = zbx
        await until(lambda _:zb.x < 121).after(134)
        end_time = fm.time
        end3 = True
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        nonlocal end4
        zb = iz_test.game_board.iz_place_zombie(3,8,ZombieType.gargantuar)
        zb.x = zbx
        await until(lambda _:zb.x < 121).after(134)
        end_time = fm.time
        end4 = True
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        nonlocal end5
        zb = iz_test.game_board.iz_place_zombie(4,8,ZombieType.gargantuar)
        zb.x = zbx
        await until(lambda _:zb.x < 121).after(134)
        end_time = fm.time
        end5 = True
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1
    
    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        nonlocal end1,end2,end3,end4,end5
        # if fm.time > 0:
        if end1 and end2 and end3 and end4 and end5:
            end1 = end2 = end3 = end4 = end5 = False
            return iz_test.end(True)
    
    iz_test.start_test(jump_frame=1, speed_rate=2, print_interval=100)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)

fin_time = times[:next( (i+1 for i in range(len(times)-1,-1,-1) if times[i]!=0 ) )]
x = np.arange(len(fin_time))
fin_time = fin_time[next((i for i in range(len(fin_time)) if fin_time[i]!=0)):]
x = x[-len(fin_time):]

values = x[fin_time>0]
counts = fin_time[fin_time>0]
total = 1.0 * test_count
mean = np.sum(values*counts) / total
print("mean: ",mean)

# vari = np.sum((values-mean)**2 * counts) / (total -1)
# std = np.sqrt(vari)
# print("std: ",std)

# coef = mean / np.sqrt(3*vari)
# print('coef:',coef)

fin_time = fin_time/total

plt.bar(x,fin_time)
plt.show()
