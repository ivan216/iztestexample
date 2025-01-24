from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
import matplotlib.pyplot as plt

full_hp = 120
test_count = 200
targ = '0'
form = 'yo...'
zb = 'tt'
oppo = '0'
start = 6
zbx = 765.0

if zbx is None:
    zbx = start * 80 - 70
hp_record = [0] * (full_hp + 1)

def fun(ctler: Controller):

    iz_test = IzTest(ctler).init_by_str(f'''
        {test_count} -1
        1-{targ} 2-{targ} 3-{targ} 4-{targ} 5-{targ}
        {(form +'\n')* 5}{(zb + ' ') * 5}
        {(oppo + ' ')*5}
        1-{start} 2-{start} 3-{start} 4-{start} 5-{start}''')
    
    iz_test.controller.write_bool(False, 0x6a66f4)
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(0)
        tt.x = zbx
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        hp_record[i] += 1
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(1)
        tt.x = zbx
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        hp_record[i] += 1

    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(2)
        tt.x = zbx
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        hp_record[i] += 1
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(3)
        tt.x = zbx
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        hp_record[i] += 1

    @iz_test.flow_factory.add_flow()
    async def _(_):
        tt = iz_test.ground.zombie(4)
        tt.x = zbx
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        hp_record[i] += 1

    iz_test.start_test(jump_frame=1, speed_rate=10, print_interval=20)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)

plt.figure(figsize=(16,12),dpi=150)
plt.bar(list(range(full_hp + 1)), [y/test_count/5 for y in hp_record])
plt.title(f"{form} ,zombie at x = {zbx} ,N = {test_count*5}")
plt.xlabel('hp (lost)')
plt.ylabel('frequency')
plt.show()
