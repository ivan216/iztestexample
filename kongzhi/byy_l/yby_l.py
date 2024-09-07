from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

##3.58倍75，共269

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        yby_l
        .....
        .....
        lz 
        0  
        3-6''')
    
    _75_count =0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count
        bu = False
        fu = False  #zb2赋值标志
        l = iz_test.ground["3-5"]
        b = iz_test.ground["3-2"]
        y = iz_test.ground["3-1"]
        lz = iz_test.game_board.zombie_list[0]

        while not l.is_dead:
            await until(lambda _:lz.hp < 90 or l.is_dead)
            if not l.is_dead :
                lz = place("lz 3-6")
                _75_count += 1

        await until(lambda _:lz.hp <= 110 or lz.int_x <= 310)  #320
        [cg1, cg2] = await repeat("cg 3-6")     #合适时机放双杆
        _75_count += 2

        await until(lambda _:cg1.butter_cd > 0 or cg2.butter_cd >0 or cg1.hp < 170 or cg2.hp < 170)
        
        if cg1.butter_cd > 0 or cg1.hp < 170 :
            zb1 = cg1   #保证zb1是第一个中黄油，或者第一个挂的僵尸
            zb2 = cg2
            if cg1.butter_cd == 0:  #没中过黄油，直接进入补刀阶段
                bu = True
        else:
            zb1 = cg2
            zb2 = cg1
            if cg2.butter_cd == 0:
                bu = True
        
        if not bu:
            if zb1.int_x >= 295:
                await until(lambda _:zb2.butter_cd >0)
                if 270 < zb2.int_x < 295 :
                    place("cg 3-6")
                    _75_count += 1 
                else:
                    fu = True
            elif 270 < zb1.int_x < 295 :
                await until(lambda _:zb2.butter_cd >0)
                if not b.is_dead:
                    place("cg 3-6")
                    _75_count += 1 
                else:
                    fu = True   #进入处理阶段
            else:
                fu = True

        if fu:  #给zb2正确赋值
            await until(lambda _:zb1.hp < 170 or zb2.hp < 170)
            if zb2.hp < 170:
                zb2 = zb1  #保证活着的僵尸是 zb2
            bu = True   #进入补刀阶段

        if bu:  #补刀阶段
            await until(lambda _:zb2.hp < 170)  #zb2一定是血最多的
            place("cg 3-6")  #zb2挂了说明没僵尸了，补杆
            _75_count += 1  #没再考虑后续补刀

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)