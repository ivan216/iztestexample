from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.structs.plant import PlantType
from rpze.structs.zombie import ZombieType
from rpze.iztest.plant_modifier import randomize_generate_cd
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
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
    async def _(_):
        iz_test.game_board.sun_num = 4321

        plist = []
        plist.append(iz_test.game_board.new_plant(2,1,PlantType.gatling_pea))
        plist.append(iz_test.game_board.new_plant(2,1,PlantType.winter_melon))
        for pl in plist:
            randomize_generate_cd(pl)
        plist.append(iz_test.game_board.new_plant(1,2,0x34)) # 反向双发
        for pl in plist:
            iz_test.game_board.iz_setup_plant(pl)

        xg = iz_test.game_board.zombie_list[0]
        xg.die_no_loot()

        jr = iz_test.game_board.iz_place_zombie(2,5,ZombieType.giga_gargantuar)
        jr.x = 800.0

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(game_path) as game:
    fun(game.controller)