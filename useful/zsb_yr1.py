from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place 
from rpze.iztest.cond_funcs import until_precise_digger, until_plant_n_shoot
from rpze.flow.utils import until 
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        5-1 4-1 3-1
        hsojt
        dlh3h
        c51__
        hbhzz
        hppwy
        cg 
        0  
        1-6''')

    _75_count = 0

    @iz_test.flow_factory.add_flow()
    async def _(_):
        magnet = iz_test.ground["3-1"]
        cg = iz_test.game_board.zombie_list[0]
        await until(lambda _:cg.int_x <=140) #140的话矿与杆基本不冲突
        place("kg 5-6")
        await until(lambda _:magnet.status_cd > 0)
        await until_precise_digger(magnet)
        place("kg 4-8")
        
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _75_count
        star = iz_test.ground["3-2"]
        o = iz_test.ground["1-3"]
        o.hp = 4    #提升测试效率
        await until_plant_n_shoot(star,2).after(55 + randint(0,10))
        cg1 = place("cg 3-6")
        await until(lambda _:cg1.hp <= 166).after(20 + randint(0,10))
        place("cg 3-6")
        _75_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(_75_count)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    