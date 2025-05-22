from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from rpze.structs.plant import PlantType
from rpze.structs.zombie import ZombieType, ZombieStatus
from rpze.flow.utils import delay,until
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler:Controller):
    iz_test = IzTest(ctler).init_by_str(
        '''
        100 -1
        
        .....
        .....
        .o...
        .....
        .....
        ''')

    kg = pl = None
    last1 = False
    print('dig:',ZombieStatus.digger_dig)
    print('drill:',ZombieStatus.digger_drill)
    print('dizzy:',ZombieStatus.digger_dizzy)
    print('walk right:',ZombieStatus.digger_walk_right)

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal kg,pl
        kg = iz_test.game_board.iz_place_zombie(2,5,ZombieType.digger)
        kg.accessories_hp_1 = 60
        kg.hp = 90

        pl = iz_test.game_board.new_plant(2,0,PlantType.gloomshroom)
        pl.hp = 1000
        pl.generate_cd = 134 #
        
        # await until(lambda _:pl.launch_cd == 57) 
        await delay(3)
        kg.x = 9.9
        
        # jing:delay1 133最早 dizzy0+1；132最晚 0+boot
        # delay1: dizzy0+352; 2: 0+351; 3: 0+350; 4: 0+353
        # dong: 最早在+1cs才能被打  42: lcd 174刚好被打 173不被打
        # hit: lcd: 126, 98, 70, 42
        # 命中第15下掉头，曾攻击优先级高于矿啃食
    
    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        if fm.time > 0:
            if kg.hp < 70:
                return iz_test.end(False)
            
    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        nonlocal last1
        if fm.time>0:
            if last1:
                pl.generate_cd = 200
                last1 = False
            if pl.generate_cd==1:
                last1 = True
            print(' time:',fm.time,' status:',kg.status,' kg_sum_hp:',kg.hp+kg.accessories_hp_1,\
                  ' pl_hp:',pl.hp,' pl_gcd:',pl.generate_cd,' pl_lcd:',pl.launch_cd)

    iz_test.start_test(jump_frame=0, speed_rate=1, print_interval=0)

with InjectedGame(game_path) as game:
    fun(game.controller)