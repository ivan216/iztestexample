from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.iztest.operations import place
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        ...wt
        .....
        ...s.
        .....
        ...s.
        lz  lz  cg  cg
        0   0   0   0
        1-6 2-6 3-6 5-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        iz_test.game_board.plant_list.set_next_idx(5)
        place("w 2-4")
        iz_test.game_board.plant_list.set_next_idx(4)   # 0~3已经被占用
        place("t 2-5")

        iz_test.game_board.plant_list.set_next_idx(8)
        j1 = place("j 3-3")
        j1.hp = 1200
        
        iz_test.game_board.plant_list.set_next_idx(7)
        tp = place("3 4-3")
        randomize_generate_cd(tp)

        iz_test.game_board.plant_list.set_next_idx(6)
        j2 = place("j 5-3")
        j2.hp = 1200

    iz_test.start_test(jump_frame=0, speed_rate=1)
    
with InjectedGame(game_path) as game:
    fun(game.controller)
    