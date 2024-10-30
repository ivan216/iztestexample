from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.flow.flow import FlowManager
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        .....
        ddpcc
        .....
        .....
        lz 
        0  
        3-6''')
    
    cg_count = 0
    bu = can_end = False

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal cg_count,bu,can_end
        bu = can_end = False
        lz=iz_test.game_board.zombie_list[0]
        c1= iz_test.ground["3-4"]
        c2=iz_test.ground["3-5"]
        d=iz_test.ground["3-2"]

        await until(lambda _:c2.is_dead).after(150)
        if lz.dx< randint(25,28)/100:   #25-28
            place("cg 3-6")    #帮挡的撑杆
            cg_count += 1
            await until(lambda _:c1.hp<150).after(randint(0,10)) #死亡？
            cg = place("cg 3-6")    
            cg_count += 1
            bu = can_end = True
            
        else:
            await until(lambda _:c1.hp<300)
            if lz.hp > 210:
                await delay(150).after(randint(0,10))    #血量健康，用预判
                cg = place("cg 3-6")
                cg_count += 1
                bu = can_end = True

            else:
                await until(lambda _:lz.hp < 90 or c1.is_dead)
                if (c1.is_dead):
                    await until_plant_last_shoot(d).after(randint(0,10)) #血量不行，用相位
                    cg = place("cg 3-6")
                    cg_count+=1
                    bu = can_end = True

                else:
                    hp = c1.hp
                    place("lz 3-6")
                    cg_count += 1
                    await until(lambda _:c1.hp<hp and c1.hp<150).after(randint(0,10))    #第二个必定健康，用帮挡
                    cg = place("cg 3-6")
                    cg_count += 1
                    bu = can_end = True
        
        if bu:  #补刀
            await until(lambda _:cg.hp < 170)
            place("cg 3-6")
            cg_count += 1
        
    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowManager):
        if can_end:
            if iz_test.ground["3-0"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(cg_count)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
