from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.structs.plant import PlantType
from rpze.structs.zombie import ZombieType
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.flow.flow import FlowManager
from random import randint

def fun(ctler:Controller):
    iz_test = IzTest(ctler).init_by_str(f'''
        1000 -1
        1-0 2-0 3-0 4-0 5-0
        b....
        .....
        .....
        .....
        .....
        lz
        0  
        3-11 ''')

    @iz_test.flow_factory.add_flow()
    async def _(_):
        pao = iz_test.game_board.new_plant(1,0,PlantType.cob_cannon)
        jr = iz_test.game_board.iz_place_zombie(0,9,ZombieType.gargantuar)
    
    iz_test.start_test(jump_frame=0, speed_rate=1, print_interval=100)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)