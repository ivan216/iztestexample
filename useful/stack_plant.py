from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.structs.plant import PlantType
from rpze.rp_extend import Controller
from rpze.iztest.plant_modifier import randomize_generate_cd

def fun(ctler: Controller):
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
        iz_test.game_board.iz_new_plant(1,3,PlantType.squash)
        iz_test.game_board.plant_list.set_next_idx(4)   # 0~3已经被占用
        iz_test.game_board.iz_new_plant(1,4,PlantType.potato_mine)

        iz_test.game_board.plant_list.set_next_idx(8)
        hs1 = iz_test.game_board.iz_new_plant(2,2,PlantType.torchwood)
        hs1.hp = 6000
        
        iz_test.game_board.plant_list.set_next_idx(7)
        tp = iz_test.game_board.iz_new_plant(3,2,PlantType.threepeater)
        randomize_generate_cd(tp)

        iz_test.game_board.plant_list.set_next_idx(6)
        hs2 = iz_test.game_board.iz_new_plant(4,2,PlantType.torchwood)
        hs2.hp = 6000

    iz_test.start_test(jump_frame=0, speed_rate=1)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    