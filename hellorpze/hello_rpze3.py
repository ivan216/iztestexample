from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        1ssss
        .....
        .....
        ''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        place("lz 3-6")

    @iz_test.flow_factory.add_tick_runner()
    def _(fm):
        if iz_test.ground["3-0"] is None:
            return iz_test.end(True)
        if fm.time > 0:
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
    
    iz_test.start_test(jump_frame=1, speed_rate=5)

with InjectedGame(game_path) as game:
    fun(game.controller)