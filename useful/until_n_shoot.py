from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place , repeat
from rpze.iztest.cond_funcs import until_precise_digger
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool ,until ,delay
from rpze.structs.plant import Plant
from rpze.rp_extend import Controller
from random import randint

def until_plant_n_shoot(plant: Plant, n:int = 1) -> AwaitableCondFunc:
    def _cond_func(fm: FlowManager,
                   v=VariablePool(try_to_shoot_time=None, shots = 0)):
        if plant.generate_cd == 1:  # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time == fm.time and plant.launch_cd != 0:  # 在攻击时
            v.shots += 1
        if v.try_to_shoot_time == fm.time and plant.launch_cd == 0: #不再攻击时，计数清零
            v.shots = 0
        if v.shots == n:
            return True
        return False
    return AwaitableCondFunc(_cond_func)

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

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        plist = iz_test.ground
        zlist = iz_test.game_board.zombie_list
        magnet = plist["3-1"]
        cg = zlist[0]
        await until(lambda _:cg.int_x <=140) #140的话矿与杆基本不冲突
        place("kg 5-6")
        await until(lambda _:magnet.status_cd > 0)
        await until_precise_digger(magnet)
        place("kg 4-8") #注意矿工和补杆没有冲突，实战时建议使用非八列矿工法
        
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        plist = iz_test.ground
        star = plist["3-2"]
        await until_plant_n_shoot(star,2).after(55 + randint(0,10))
        cg1 = place("cg 3-6")
        await until(lambda _:cg1.hp <= 166).after(20 + randint(0,10))
        place("cg 3-6")

    iz_test.start_test(jump_frame=0, speed_rate=3)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    