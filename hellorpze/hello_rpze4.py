from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.iztest.operations import place
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler)

    @iz_test.flow_factory.add_flow()
    async def _(_):
        place("lz 3-6")
        df = place("1 3-1")
        randomize_generate_cd(df)
        place("s 3-2")
        place("s 3-3")
        place("s 3-4")
        place("s 3-5")
        
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
    