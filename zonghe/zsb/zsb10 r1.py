from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.structs.plant import Plant , PlantStatus

def count_butter(plant: Plant, n:int = 1, non_stop: bool = True, continuous: bool = False) -> AwaitableCondFunc[None]:         #通过状态数黄油数量
    def _cond_func(fm: FlowManager,v = VariablePool(projs = 0, try_to_shoot_time=None)):
        if plant.generate_cd == 1:                                      # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time == fm.time :
            if plant.status is PlantStatus.kernelpult_launch_butter :
                v.projs += 1
            elif plant.launch_cd == 0 :
                if non_stop or continuous:
                    v.projs = 0
            else:
                if continuous:
                    v.projs = 0
        if v.projs == n:
            return True 
        return False
    return AwaitableCondFunc(_cond_func)

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0
        y_p_h
        dpczh
        bs5tz
        13jlo
        ppwph
        tt 
        0  
        1-6 ''')
    
    cg_count =0
    xg_count =0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal cg_count,xg_count
        tt = iz_test.game_board.zombie_list[0]       
        plist = iz_test.ground
        h = plist["1-5"]
        c = plist["2-3"]
        y = plist["1-1"]
        
        await (until(lambda _:h.is_dead or tt.hp <90) | count_butter(y,2).after(142))
        if h.is_dead:
            await until(lambda _:tt.hp <= 110 or tt.int_x <= 330)
            cg = place("cg 1-6")
            cg_count += 1
        else:
            place("xg 1-6")
            xg_count += 1
            await until(lambda _:h.is_dead)
            cg = place("cg 1-6")
            cg_count += 1

        while not y.is_dead:
            await until(lambda _:cg.hp < 170)
            cg = place("cg 1-6")
            cg_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(cg_count)
    print(xg_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)