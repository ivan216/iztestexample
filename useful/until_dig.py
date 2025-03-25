from rpze.flow.utils import AwaitableCondFunc
from rpze.structs.plant import Plant
from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from rpze.iztest.operations import place
from rpze.flow.utils import delay

def until_precise_digger(magnet: Plant, interval: int = 912) -> AwaitableCondFunc[None]:
    """
    生成一个等到磁铁到达精确矿时间的函数

    Args:
        magnet: 要判断 cd 的磁铁
        interval: 等价操作间隔. 于0cs磁铁空闲时释放铁器, 在912-915cs于6列释放的矿工被视为1列精确矿, 该释放时机称作等价操作间隔
    """
    return AwaitableCondFunc(lambda _: magnet.status_cd <= 1502 - interval)

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        ....t
        bl.c.
        .....
        .....
        tz 
        0  
        2-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        c = iz_test.ground["3-4"]
        await delay(1)
        await until_precise_digger(c,912)
        place("kg 3-6")
    
    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        if iz_test.ground["3-0"] is None :
            return iz_test.end(True)
        if fm.time > 1600:
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
            
    iz_test.start_test(jump_frame=1, speed_rate=5)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)