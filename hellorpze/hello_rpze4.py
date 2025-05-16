from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.structs.plant import PlantType
from rpze.structs.zombie import ZombieType
from rpze.iztest.plant_modifier import randomize_generate_cd
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler)

    @iz_test.flow_factory.add_flow()
    async def _(_):
        iz_test.game_board.iz_place_zombie(2,5,ZombieType.conehead)

        iz_test.game_board.iz_new_plant(2,1,PlantType.umbrella_leaf)
        iz_test.game_board.iz_new_plant(2,2,PlantType.umbrella_leaf)
        iz_test.game_board.iz_new_plant(2,3,PlantType.umbrella_leaf)
        iz_test.game_board.iz_new_plant(2,4,PlantType.umbrella_leaf)
        randomize_generate_cd(iz_test.game_board.iz_new_plant(2,0,PlantType.pea_shooter))
    
    @iz_test.flow_factory.add_tick_runner()
    def _(fm):
        if fm.time > 0:
            if iz_test.ground["3-0"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
    
    @iz_test.check_tests_end()
    def _(n,ns):
        if n < 1e3:
            return None
        return ns/n
    
    iz_test.start_test(jump_frame=True, speed_rate=5, print_interval=1e1)

with InjectedGame(game_path) as game:
    fun(game.controller)
    