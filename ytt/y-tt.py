from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
import matplotlib.pyplot as plt

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        -1 -1
        3-0
        .....
        .....
        yssss
        .....
        .....
        tt
        0  
        3-6 ''')
    
    full_hp = 70
    test_count = 10000
    hp_count = [0 for _ in range(full_hp)]
    x = list(range(full_hp))
    sum = 0
    zb = None
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal zb
        zb = iz_test.game_board.zombie_list[0]
        zb.accessories_hp_1 = full_hp * 20

    @iz_test.on_game_end()
    def end_callback(result: bool):
        nonlocal sum
        plist = iz_test.ground
        if plist["3-1"] is None:
            i = (full_hp * 20 - zb.accessories_hp_1) // 20
            sum += i
            hp_count[i] += 1 
        
    @iz_test.check_tests_end()
    def end_test_callback(n, ns):
        if n%100 == 0:
            print("每100次输出当前期望： ",sum / n)
        if n < test_count:
            return None
        return True

    iz_test.start_test(jump_frame=1, speed_rate=5)
    
    print(sum / test_count)
    print(hp_count)

    plt.figure(1)
    plt.bar(x,hp_count,color='blue')

    plt.show()

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
