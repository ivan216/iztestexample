from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place ,repeat
from rpze.flow.utils import until, delay
from rpze.rp_extend import Controller
from random import randint

# 75 + 50*0.02 + 75* 2.04 +125*0.344 = 272

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        byy_l
        .....
        .....
        lz 
        0  
        3-6''')
    
    _75_count = 0
    _50_count = 0
    _125_count = 0
    x_c = 295
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _75_count,_50_count,_125_count
        bu = pan = False
        lz = iz_test.game_board.zombie_list[0]
        l = iz_test.ground["3-5"]
        b = iz_test.ground["3-1"]
        y1 = iz_test.ground["3-2"]
        y2 = iz_test.ground["3-3"]

        await until(lambda _:lz.hp < 90 or l.is_dead)
        if l.is_dead:
            await until(lambda _: lz.hp <= 110 or lz.int_x <= 320)
            [cg1, cg2] = await repeat("cg 3-6")     #合适时机放双杆
            _75_count += 2

            await until(lambda _: cg1.butter_cd == 400 or cg2.butter_cd == 400 or cg1.hp < 170 or cg2.hp < 170)
                
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

            if not bu:  #还没到补刀阶段
                if  270 < zb1.int_x < x_c:   #刺上中黄油，补杆
                    place("cg 3-6")     #没有再考虑后续补刀
                    _75_count += 1
                elif zb1.int_x >= x_c:  #刺外中黄油
                    await until(lambda _:zb2.butter_cd == 400 or zb1.butter_cd == 400)  #中第二黄油
                    if zb1.butter_cd == 400 and zb1.int_x > 270 or zb2.butter_cd == 400 and zb2.int_x > 270 : #起跳前中
                        place("cg 3-6")
                        _75_count += 1
                    else:   #第二黄油不在起跳前中，可以继续等待
                        pan = True
                else:   #跳跃后才中黄油或者没中过黄油
                    pan = True

            if pan: #把血最多的僵尸赋值给zb2
                await until(lambda _:zb1.hp < 170 or zb2.hp < 170)
                if zb2.hp < 170:
                    zb2 = zb1  #保证活着的僵尸是 zb2
                bu = True   #进入补刀阶段

            if bu:  #补刀阶段
                await until(lambda _:zb2.hp < 170)  #zb2一定是血最多的
                await repeat("cg 3-6")  #zb2挂了说明没僵尸了，补双杆
                _75_count += 2  #没再考虑后续补刀
        else:
            kg = place("kg 3-6")
            _125_count += 1
            await until(lambda _: b.hp < 20 ) #20 90%
            while not l.is_dead:
                lz = place("lz 3-6")
                _75_count += 1
                await until(lambda _:lz.hp < 90 or l.is_dead)
            
            await until(lambda _:lz.hp < 90)
            if not y2.is_dead or not b.is_dead :
                place("cg 3-6")
                _75_count += 1
            else:
                place("xg 3-6")
                _50_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=10)
    print(_50_count)
    print(_75_count)
    print(_125_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)