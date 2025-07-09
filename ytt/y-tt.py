from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import nbinom

full_hp_count = 150
full_hp = 20*full_hp_count
# test_count = 100000
test_count = 100000
hurts = np.zeros(full_hp_count,dtype=int)
# basic_time = 3900  # 测试结果
basic_time = 5200

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str(f'''
        {test_count//5} -1
        1-0 2-0 3-0 4-0 5-0
        y....
        y....
        y....
        y....
        y....
        tt tt tt tt tt
        0 0 0 0 0
        1-6 2-6 3-6 4-6 5-6''')
    
    # yssss
    zbx = 765.0
    
    iz_test.controller.write_bool(False, 0x6a66f4)

    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(0)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:tt.x < 10)
        i = (full_hp - tt.accessories_hp_1) // 20
        hurts[i] += 1
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(1)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:tt.x < 10)
        i = (full_hp - tt.accessories_hp_1) // 20
        hurts[i] += 1

    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(2)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:tt.x < 10)
        i = (full_hp - tt.accessories_hp_1) // 20
        hurts[i] += 1

    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(3)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:tt.x < 10)
        i = (full_hp - tt.accessories_hp_1) // 20
        hurts[i] += 1

    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(4)
        tt.accessories_hp_1 = full_hp
        tt.x = zbx
        await until(lambda _:tt.x < 10)
        i = (full_hp - tt.accessories_hp_1) // 20
        hurts[i] += 1

    iz_test.start_test(jump_frame=1, speed_rate=5, print_interval=200)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)

hurts = hurts[:next( (i+1 for i in range(len(hurts)-1,-1,-1) if hurts[i]!=0 ) )]
hurts_prob = hurts / test_count
x = np.arange(len(hurts))

values = x[hurts>0]
counts = hurts[hurts>0]
total = 1.0 * test_count
mean = np.sum(values*counts) / total
vari = np.sum((values-mean)**2 * counts) / (total -1)
r = mean**2/(mean+vari)
p = mean/(mean+vari)
std = np.sqrt(vari)
thrid_moment = np.sum((values - mean)**3 * counts)
skewness = (thrid_moment / std**3) * (total / ((total-1)*(total-2)) )
print("mean:",mean," vari:",vari," skew:",skewness)
print("r:",r," p:",p)

nb_pmf = nbinom.pmf(x,r,p,loc=round(r))


wd_count = (basic_time - 71) / 143
r_approx: int = np.around(wd_count / 2.93).astype(int)
mean_approx = wd_count * 4688/3195 *1.25 *143/293
p_approx = r_approx / mean_approx
# var_approx = r_approx*(1-p_approx) / p_approx**2  # 化简后得下式
var_approx = mean_approx * (4688/3195 *1.25 *1.43 - 1)  # 当大于200s时越来越不准确
nb_pmf_app = nbinom.pmf(x,r_approx,p_approx,loc=round(r_approx))

print('mean_approx:',mean_approx,' var_approx:',var_approx)
print('r_approx:',r_approx, ' p_approx:',p_approx)

plt.figure(figsize=(8,6),dpi=150)
# plt.plot(x,nb_pmf_app,color='r',label='approx')
plt.plot(x,nb_pmf,color='g',label='real_app')
plt.bar(x,hurts_prob,label='real')
plt.title(f'real test count = {test_count}')
plt.legend()
plt.xlabel('dmg')
plt.ylabel('frequency')
plt.show()
