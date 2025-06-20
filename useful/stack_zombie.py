from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import delay
from rpze.iztest.operations import place
from rpze.iztest.cond_funcs import until_plant_n_shoot
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        1-2
        zzh31
        ...yw
        .....
        .....
        .....
        lz
        0
        5-9''') #2024图九；2021特殊一
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        tp = iz_test.ground["1-4"]
        xg = place("xg 2-6")
        await until_plant_n_shoot(tp).after(34) #豌豆生成

        await delay(92)       
        # if not xg.is_dead:    # BV1LH4y1h7tq 认为的处理方法
        #     await delay(143)  # 实际上对过率没有显著影响

        iz_test.game_board.zombie_list.set_next_idx(4)
        place("xg 1-6")

        await delay(48)
        iz_test.game_board.zombie_list.set_next_idx(3)
        place("xg 1-6")

        await delay(118)
        iz_test.game_board.zombie_list.set_next_idx(2)
        place("xg 1-6")

    iz_test.start_test(jump_frame=1, speed_rate=1, print_interval=1e2)

with InjectedGame(game_path) as game:
    fun(game.controller)
    