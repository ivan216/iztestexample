from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot,until_plant_die
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowFactory
from rpze.structs.zombie import ZombieStatus
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        .....
        dcddd
        .....
        .....
        lz 
        0  
        3-6''')
    
    _75_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count
        d1 = iz_test.ground["3-1"]
        d3 = iz_test.ground["3-3"]

        await until_plant_last_shoot(d3).after(randint(0,10))
        cg = place("cg 3-6")
        _75_count += 1

        while iz_test.ground["3-1"] is not None:
            await until(lambda _:cg.status is ZombieStatus.pole_vaulting_walking)
            await until_plant_last_shoot(d1).after(randint(0,10))
            cg = place("cg 3-6")
            _75_count += 1

    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowFactory):
        if iz_test.ground["3-0"] is None:
            return iz_test.end(True)
        if fm.time > 10000: #防止死循环
            return iz_test.end(False)
        
    iz_test.start_test(jump_frame=1, speed_rate=2)
    print(_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)