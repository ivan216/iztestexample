from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        -1 -1
        3-0
        .....
        .....
        1ssss
        .....
        .....
        tt
        0  
        3-6 ''')
    
    full_hp = 40    #给铁桶多少血
    test_count = 1000   #测试次数
    hp_record = [0 for x in range(0,full_hp)]    #记录伤害情况
    sum = 0     #受伤总数，用来最后求平均
    zb = None

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal zb
        zb = iz_test.game_board.zombie_list[0]
        zb.accessories_hp_1 = full_hp * 20

    @iz_test.on_game_end()
    def end_callback(result: bool):
        nonlocal hp_record,sum
        i = (full_hp * 20 - zb.accessories_hp_1) // 20
        sum += i
        hp_record[i] += 1

    @iz_test.check_tests_end()
    def end_test_callback(n, ns):
        nonlocal test_count,sum
        if n%100 == 0:
            print("每100次输出当前期望： ",sum / n)
        if n < test_count:
            return None
        return True
    
    iz_test.start_test(jump_frame=1, speed_rate=5)

    print(sum / test_count)
    print(hp_record)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
