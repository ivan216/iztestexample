from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
import matplotlib.pyplot as plt

full_hp = 70
test_count = 200
hp_count = [0 for _ in range(full_hp)]

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str(f'''
        {test_count} -1
        1-0 2-0 3-0 4-0 5-0
        yssss
        yssss
        yssss
        yssss
        yssss
        tt tt tt tt tt
        0 0 0 0 0
        1-6 2-6 3-6 4-6 5-6''')
    
    iz_test.controller.write_bool(False, 0x6a66f4)

    sum = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal sum
        tt = iz_test.ground.zombie(0)
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        sum += i
        hp_count[i] += 1
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal sum
        tt = iz_test.ground.zombie(1)
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        sum += i
        hp_count[i] += 1

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal sum
        tt = iz_test.ground.zombie(2)
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        sum += i
        hp_count[i] += 1

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal sum
        tt = iz_test.ground.zombie(3)
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        sum += i
        hp_count[i] += 1

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal sum
        tt = iz_test.ground.zombie(4)
        tt.accessories_hp_1 = full_hp * 20

        await until(lambda _:tt.x < 10)
        i = (full_hp * 20 - tt.accessories_hp_1) // 20
        sum += i
        hp_count[i] += 1
        
    @iz_test.on_game_end()
    def _(_):
        if iz_test._test_time % 200 == 199:
            n = iz_test._test_time + 1
            print(f"当前次数: {n*5} ,当前期望: {sum/n/5}")

    iz_test.start_test(jump_frame=1, speed_rate=5, print_interval=200)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)

plt.figure(1)
plt.bar(list(range(full_hp)), [y/test_count/5 for y in hp_count])
plt.title('yssss , zombie at col 6, N = ' + str(test_count*5) )
plt.xlabel('hp (lost)')
plt.ylabel('frequency')
plt.show()
