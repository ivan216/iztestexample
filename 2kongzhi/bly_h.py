from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool ,until
from rpze.structs.plant import Plant
from rpze.structs.projectile import ProjectileType
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        bly_h
        .....
        .....
        tz  
        0  
        3-6 ''')
    
    def count_butter2(plant: Plant, n:int = 1) -> AwaitableCondFunc:         #通过子弹数黄油数量
        def _cond_func(fm: FlowManager,v = VariablePool( projs = 0, count_down = 0,try_to_shoot_time=None)):
            if plant.is_dead :
                return False
            if plant.generate_cd == 1:                                      # 下一帧可能开打
                v.try_to_shoot_time = fm.time + 1
            if (v.try_to_shoot_time == fm.time) and (plant.launch_cd == 0): #并没有攻击，计数重置
                v.projs = 0
                v.count_down = 0
            if (v.try_to_shoot_time == fm.time) and (plant.launch_cd != 0): #确定要攻击，把launch_cd传给count_down
                v.count_down = plant.launch_cd
            if v.count_down == 1 :                                          #在count_down到1时，黄油才可以被获得。
                for proj in ~iz_test.game_board.projectile_list:
                    if proj.type_ == ProjectileType.butter :
                        v.projs += 1
            if v.projs == n:
                return True 
            if v.count_down !=0:
                v.count_down -= 1
            return False
        return AwaitableCondFunc(_cond_func)
    
    _75_count = 0
    _150_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count,_150_count
        y = iz_test.ground["3-3"]
        l = iz_test.ground["3-2"]
        tz = iz_test.game_board.zombie_list[0]

        # 不出黄油必过
        await until(lambda _:tz.butter_cd > 399)
        if tz.x > 300:  #刺外
            await (until(lambda _:l.hp < 300) | count_butter2(y))
            if l.hp == 300: #出第二黄油
                place("tz 3-6")
                _150_count += 1
            else :  #没再出黄油
                place("cg 3-6")
                _75_count += 1
        elif tz.x > 220 :   #刺上
            await (until(lambda _:tz.accessories_hp_2 < 1) | count_butter2(y))
            if tz.accessories_hp_2 == 0:    #没再出黄油
                if l.hp > 140 :     #不可补杆 140
                    place("tz 3-6")
                    _150_count += 1
                else:               #可补杆
                    place("cg 3-6")
                    _75_count += 1
            else:               #出第二黄油
                place("tz 3-6")
                _150_count += 1
        else:       #已走出地刺
            await until(lambda _:l.hp < 300)
            place("cg 3-6")
            _75_count += 1
    
    iz_test.start_test(jump_frame=1, speed_rate=2)
    print("补杆：",_75_count)
    print("补梯：",_150_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)