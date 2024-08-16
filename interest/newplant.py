from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.structs.plant import PlantType
from rpze.structs.zombie import ZombieType
from rpze.iztest.plant_modifier import randomize_generate_cd

def fun(ctler:Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
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
    async def place_zombie(_):
        iz_test.game_board.sun_num = 4321

        jq = iz_test.game_board.new_plant(2,1,PlantType.gatling_pea)
        iz_test.game_board.iz_setup_plant(jq)
        randomize_generate_cd(jq)
        bg = iz_test.game_board.new_plant(2,1,PlantType.winter_melon)
        iz_test.game_board.iz_setup_plant(bg)
        randomize_generate_cd(bg)
        fs = iz_test.game_board.new_plant(1,2,0x34)
        iz_test.game_board.iz_setup_plant(fs)

        xg = iz_test.game_board.zombie_list[0]
        xg.die_no_loot()

        jr = iz_test.game_board.iz_place_zombie(2,5,ZombieType.giga_gargantuar)
        jr.x = 800.0

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)