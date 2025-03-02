from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.structs.plant import PlantType
from rpze.structs.zombie import ZombieType
from rpze.iztest.plant_modifier import randomize_generate_cd
from random import randint

def fun(ctler:Controller):
    iz_test = IzTest(ctler).init_by_str('''
        100 -1
        3-0
        .....
        .....
        .....
        .....
        .....
        xg
        0  
        1-6 ''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        for _ in range(10):
            randomize_generate_cd(iz_test.game_board.new_plant(2,0,PlantType.kernelpult))
        jr = iz_test.game_board.iz_place_zombie(2,5,ZombieType.giga_gargantuar)
        jr.x = randint(845,854)
        jr.hp = 200000

    iz_test.start_test(jump_frame=1, speed_rate=10,print_interval=10)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)