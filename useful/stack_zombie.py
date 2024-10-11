from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import delay
from rpze.iztest.operations import place
from rpze.iztest.cond_funcs import until_plant_n_shoot

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
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
    async def place_zombies(_):
        tp = iz_test.ground["1-4"]
        place("xg 2-6")
        await until_plant_n_shoot(tp).after(34) #豌豆生成
        await delay(92)

        iz_test.game_board.zombie_list.set_next_idx(4)
        place("xg 1-6")

        await delay(48)
        iz_test.game_board.zombie_list.set_next_idx(3)
        place("xg 1-6")

        await delay(118)
        iz_test.game_board.zombie_list.set_next_idx(2)
        place("xg 1-6")

    iz_test.start_test(jump_frame=1, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    