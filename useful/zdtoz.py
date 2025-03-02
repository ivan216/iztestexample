from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place ,repeat
from rpze.flow.utils import until 
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.flow.flow import FlowManager
from rpze.rp_extend import Controller
from rpze.structs.plant import PlantStatus

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        zdtoz
        .....
        .....
        .....
        .....
        xg 
        0  
        1-7''')

    dz_eat = 0

    @iz_test.flow_factory.add_flow()
    async def _(_):
        d = iz_test.ground["1-2"]
        z = iz_test.ground["1-5"]

        await until_plant_last_shoot(d)
        await repeat("lz 1-6")
        await until(lambda _:z.hp < 12)
        place("cg 1-6")
    
    @iz_test.on_game_end()
    def _(res:bool):
        nonlocal dz_eat
        if not res:
            if iz_test.ground["1-1"].status is PlantStatus.chomper_bite_success:
                dz_eat += 1

    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        if iz_test.ground["1-0"] is None:
            return iz_test.end(True)
        if fm.time > 1000:
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(dz_eat)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
