from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.structs.plant import Plant, PlantType, PlantStatus
from rpze.structs.zombie import  Zombie, ZombieType
from rpze.flow.utils import AwaitableCondFunc,FlowManager,VariablePool,until
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def until_zombie_dying(zombie: Zombie) -> AwaitableCondFunc[None]:
    """
    生成一个等到"僵尸 正在死亡/已死亡"的函数

    Args:
        zombie: 要判断的僵尸
    """
    return AwaitableCondFunc(lambda _: not zombie.is_not_dying or zombie.is_dead)

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0
        .....
        .....
        .....
        .....
        .....
        xg lz 
        0  0
        3-6 2-9''')
    
    zb = None

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal zb
        zb = iz_test.ground.zombie(0)
        pl = place("z 3-4")
        await until_zombie_dying(zb)
        place("lz 4-6")
    
    @iz_test.flow_factory.add_tick_runner()
    def _(fm):
        if fm.time>0:
            print(fm.time," ", zb.is_dead)

    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(game_path) as game:
    fun(game.controller)