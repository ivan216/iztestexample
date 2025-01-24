from rpze.basic.inject import InjectedGame
from rpze.rp_extend import Controller
from rpze.iztest.iztest import IzTest
from rpze.flow.flow import FlowManager
from rpze.structs.plant import PlantType,Plant
from rpze.structs.zombie import ZombieType,Zombie
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.flow.utils import delay
from random import randint

def fun(ctler:Controller):
    iz_test = IzTest(ctler)
    iz_test.controller.write_bool(False, 0x6a66f4)

    kg_l :list[Zombie]= []
    pl_l :list[Plant]= []
    hp_r = [0] * 4
    test_count = int(2e5)

    @iz_test.flow_factory.add_flow()
    async def _(_):
        for i in [0,2,4]:
            kg_l.append(iz_test.game_board.iz_place_zombie(i,5,ZombieType.digger)) 
            pl_l.append(randomize_generate_cd(iz_test.game_board.new_plant(i,0,PlantType.gloomshroom)))  
            for _ in range(3):
                randomize_generate_cd(iz_test.game_board.new_plant(i,1,PlantType.gloomshroom))

    @iz_test.flow_factory.add_flow()
    async def _(_):
        await delay(randint(1,4))
        kg_l[0].x = 9.9
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        await delay(randint(1,4))
        kg_l[1].x = 9.9
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        await delay(randint(1,4))
        kg_l[2].x = 9.9

    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        if fm.time > 0:
            if kg_l[0].hp < 90 and kg_l[1].hp < 90 and kg_l[2].hp < 90:
                return iz_test.end(False)
    
    @iz_test.on_game_end()
    def _(_):
        for k in range(3):
            if pl_l[k].hp < 300:
                i = (300 - pl_l[k].hp) // 4
                hp_r[i] += 1
        kg_l.clear()
        pl_l.clear()
    
    @iz_test.check_tests_end()
    def _(n,_):
        if n % 1e4 == 0:
            hurt_count = sum(hp_r)
            print(f"测试次数: {3*n}, 受伤次数: {hurt_count}, 受伤率: {hurt_count/n/3:.3%}")
        if n < test_count:
            return None
        return hurt_count/n/3
    
    iz_test.start_test(jump_frame=1, speed_rate=2, print_interval=1e3)
    print("受伤情况(从0开始, 间隔4): ",hp_r)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
