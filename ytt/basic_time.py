from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until,FlowManager
from rpze.iztest.operations import place
import matplotlib.pyplot as plt
import numpy as np

full_hp = 2000
test_count = 2000
times = np.zeros(10000,dtype=int)

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str(f'''
        {test_count} -1
        1-1 2-1 3-1 4-1 5-1
        1ssss
        1ssss
        1ssss
        1ssss
        1ssss
        tt tt tt tt tt
        0 0 0 0 0
        1-6 2-6 3-6 4-6 5-6''')
    
    # zbx = 765.0
    zbcol = 7
    zbx = (zbcol-1)*80 + 10.0
    
    # @iz_test.flow_factory.add_flow()
    # async def _(_):
    #     for i in range(1,6):
    #         for j in range(2,zbcol):
    #             place(f's {i}-{j}')
    
    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['1-1']
        tt = iz_test.ground.zombie(0)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1
    
    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['2-1']
        tt = iz_test.ground.zombie(1)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['3-1']
        tt = iz_test.ground.zombie(2)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['4-1']
        tt = iz_test.ground.zombie(3)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1

    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        pl = iz_test.ground['5-1']
        tt = iz_test.ground.zombie(4)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:pl.is_dead)
        end_time = fm.time
        while end_time>=len(times):
            np.append(times,np.zeros(1000,dtype=int))
        times[end_time] += 1
    
    iz_test.start_test(jump_frame=1, speed_rate=2, print_interval=100)

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
vari = np.sum((values-mean)**2 * counts) / (total -1)
std = np.sqrt(vari)
print("mean: ",mean)
print("std: ",std)

coef = mean / np.sqrt(3*vari)
print('coef:',coef)

fin_time = fin_time/total

plt.bar(x,fin_time)
plt.show()
