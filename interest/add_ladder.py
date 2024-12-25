from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.structs.plant import PlantType

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        .....
        .t.s.
        .....
        tt
        0  
        1-9 ''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        ng = iz_test.game_board.new_plant(2,2,PlantType.pumpkin)
        iz_test.game_board.iz_setup_plant(ng)

        yy = iz_test.game_board.new_plant(2,2,PlantType.gloomshroom)
        iz_test.game_board.iz_setup_plant(yy)

        dc = iz_test.game_board.new_plant(2,6,PlantType.spikerock)
        iz_test.game_board.iz_setup_plant(dc)
        
        pao = iz_test.game_board.new_plant(3,6,PlantType.cob_cannon)
        iz_test.game_board.iz_setup_plant(pao)
        
        iz_test.game_board.add_ladder(2,2)
        iz_test.game_board.add_ladder(2,6)
        iz_test.game_board.add_ladder(3,1)
        iz_test.game_board.add_ladder(3,2)
        iz_test.game_board.add_ladder(3,3)
        iz_test.game_board.add_ladder(3,6)
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)