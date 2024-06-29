from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.structs.zombie import ZombieStatus,Zombie
from rpze.structs.plant import Plant
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.rp_extend import Controller


def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0 2-0
        .....
        .....
        .....
        .....
        .....
        mj 
        0  
        1-9''')
    #尽快召唤
    #控制发愣
    #跳过召唤

    def walk_until_int_x(mj :Zombie,intx :int = 40) -> AwaitableCondFunc:
        def _cond_func(fm: FlowManager):
            if mj.int_x > intx:
                iz_test.game_board.mj_clock = 238
                return False
            return True
        return AwaitableCondFunc(_cond_func)

    def dance_until_time_step(mj :Zombie,time :int = 920) ->AwaitableCondFunc:
        def _cond_func(fm: FlowManager,v=VariablePool(vtime = time)):
            v.vtime -= 1
            if v.vtime > 0:
                iz_test.game_board.mj_clock = 450
            if v.vtime == 0:
                return True
            return False
        return AwaitableCondFunc(_cond_func)

    def keep_walking() ->AwaitableCondFunc:
        def _cond_func(fm: FlowManager):
            iz_test.game_board.mj_clock = 238 # 459,0 ~ 238
            return False
        return AwaitableCondFunc(_cond_func)

    def keep_dancing() ->AwaitableCondFunc:
        def _cond_func(fm: FlowManager):
            iz_test.game_board.mj_clock = 458 #239 ~ 458
            return False
        return AwaitableCondFunc(_cond_func)

    def partner_go_forward_together(mj:Zombie) ->AwaitableCondFunc:
        def _cond_func(fm:FlowManager):
            if mj.status == ZombieStatus.dancing_summoning:
                iz_test.game_board.mj_clock = 238
            return False
        return AwaitableCondFunc(_cond_func)

    def dance_until_partner_dead(wb:Zombie) ->AwaitableCondFunc:
        def _cond_func(fm:FlowManager):
            if not wb.is_dead:
                iz_test.game_board.mj_clock = 458
                return False
            return True
        return AwaitableCondFunc(_cond_func)

    def partner_go_forward_only_until_intx(mj:Zombie,intx: int =40) ->AwaitableCondFunc:
        def _cond_func(fm:FlowManager,v=VariablePool(last_frame_alive=False)):
            wb = iz_test.game_board.zombie_list.find(mj.partner_ids[2])
            if wb and (mj.status ==ZombieStatus.dancing_walking):
                iz_test.game_board.mj_clock = 239
            if wb:
                v.last_frame_alive = True
            if v.last_frame_alive and (not wb) :
                iz_test.game_board.mj_clock = 158 #小于159才能召唤
                v.last_frame_alive = False
            if mj.status == ZombieStatus.dancing_summoning:
                iz_test.game_board.mj_clock = 238
            if mj.int_x < intx :
                return True
            return False
        return AwaitableCondFunc(_cond_func)

    def partner_go_forward_only_until_plant_die(mj:Zombie,pl: Plant) ->AwaitableCondFunc:
        def _cond_func(fm:FlowManager,v=VariablePool(last_frame_alive=False)):
            wb = iz_test.game_board.zombie_list.find(mj.partner_ids[2])
            if wb and (mj.status ==ZombieStatus.dancing_walking):
                iz_test.game_board.mj_clock = 239
            if wb:
                v.last_frame_alive = True
            if v.last_frame_alive and (not wb) :
                iz_test.game_board.mj_clock = 158 #小于159才能召唤
                v.last_frame_alive = False
            if mj.status == ZombieStatus.dancing_summoning:
                iz_test.game_board.mj_clock = 238
            if pl.is_dead :
                return True
            return False
        return AwaitableCondFunc(_cond_func)
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        zlist = iz_test.game_board.zombie_list
        mj = zlist[0]
        await keep_walking()

    iz_test.start_test(jump_frame=0, speed_rate=3)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
