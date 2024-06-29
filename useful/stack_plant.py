from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.structs.plant import PlantType
from rpze.rp_extend import Controller

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0
        .....
        .....
        ...t.
        .....
        .....
        lz lz
        0  0
        2-7 3-7''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombies(_):
        iz_test.game_board.plant_list.set_next_idx(2)
        iz_test.game_board.iz_new_plant(1,3,PlantType.squash)
        iz_test.game_board.plant_list.set_next_idx(1)   # 0已经被占用
        iz_test.game_board.iz_new_plant(1,4,PlantType.potato_mine)

    iz_test.start_test(jump_frame=False, speed_rate=2)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    