from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.structs.zombie import ZombieStatus
from rpze.structs.plant import PlantType, Plant
from rpze.flow.flow import FlowManager
from random import randint

## gloom launch : 200   落稳再下一cs才能打中

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-2
        .....
        .....
        .o...
        .....
        .....
        xt 
        0  
        3-2 ''')
    
    yy = None
    shoot = 0
    pri = True
    
    @iz_test.flow_factory.add_flow()
    async def _(fm:FlowManager):
        nonlocal yy, shoot, pri
        shoot = 0
        pri = True
        zb = iz_test.game_board.zombie_list[0]
        yy = iz_test.game_board.new_plant(2,0,PlantType.gloomshroom)
        yy2 = iz_test.game_board.new_plant(1,0,PlantType.gloomshroom)
        yy3 = iz_test.game_board.new_plant(3,0,PlantType.gloomshroom)

        await until(lambda _:zb.status is ZombieStatus.bungee_body_drop)
        await delay(186)
        yy.generate_cd = yy2.generate_cd = yy3.generate_cd = 2
        await delay(1)  #186(+1) -- 2
        if zb.status is ZombieStatus.bungee_body_drop:
            yy.generate_cd = yy2.generate_cd = yy3.generate_cd = 2

        # await until(lambda _:zb.status is ZombieStatus.bungee_idle_after_drop)
        # yy.generate_cd = 200
    
    # @iz_test.flow_factory.add_tick_runner()
    # def _(fm:FlowManager):
    #     nonlocal shoot, pri
    #     if fm.time > 0:
    #         if yy.generate_cd == 1:
    #             shoot = fm.time + 1
    #         if shoot == fm.time and yy.launch_cd == 200:
    #             if pri:
    #                 pri = False
    #                 print("植物攻击 ",fm.time)

    # @iz_test.flow_factory.add_tick_runner()
    # def _(fm:FlowManager):
    #     if fm.time > 0:
    #         print("\033[2A\r\033[K"+"generate: ",yy.generate_cd)
    #         print("\033[K"+"launch: ",yy.launch_cd)

    iz_test.start_test(jump_frame=0, speed_rate=5)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
