from rpze.basic import*
from rpze.flow import*
from rpze.iztest import*
from rpze.structs import*
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        1-2
        zzh31
        ...yw
        .....
        .....
        .....
        xt
        0
        5-1''') #2024图九；2021特殊一

    @iz_test.flow_factory.add_flow()
    async def _(_):
        sx = iz_test.ground["1-4"]
        df = iz_test.ground["1-5"]
        place("xg 2-6")
        await until_plant_n_shoot(sx).after(50) #豌豆生成

        iz_test.game_board.zombie_list.set_next_idx(4)
        place("xg 1-6")

        b = True
        for i in range(0,58):
            if df.launch_cd == 35:
                b = False
            if i == 8:
                iz_test.game_board.zombie_list.set_next_idx(3)
                place("xg 1-6")
            await delay(1)
        c = False
        for i in range(0,20):
            if df.launch_cd == 35:
                c = True
            await delay(1)

        if b and c:
            await delay(10)
            iz_test.game_board.zombie_list.set_next_idx(2)
            place("xg 1-6")
        else:
            await delay(70)
            iz_test.game_board.zombie_list.set_next_idx(2)
            place("xg 1-6")

    iz_test.start_test(jump_frame=1, speed_rate=1)

with InjectedGame(game_path) as game:
    fun(game.controller)
