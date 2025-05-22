# 单矿工伤害测试程序
from random import randint
import numpy as np
import matplotlib.pyplot as plt

a = 1
n = 5
test_N = a * 10**n  # 测试次数

num_al = 1
num_not_al = 2  # 静曾

plant_list = [[True]]*num_al+[[False]]*num_not_al

M_sup = 1000
M = M_sup   #时间长度
###

class IO:
    def __init__(self,al):
        self.list = []
        self.start = 0
        self.list = self.hit_list(al,[158,130,102,74],200,20)  # 74是第一次命中
    @staticmethod
    def hit_list(always, hit, max_cd, dmg):
        tmp = np.zeros(M)                # 存储具体时间点的伤害
        interval = randint(max_cd-14,max_cd)  # 186-200
        # start 上一次判定到当前时刻过了多久
        # t 距离下一次判定的时长

        # fix
        prob = randint(0,(max_cd-7)*15-1)    # 0-2894
        if prob<15*(max_cd-14):
            t = 1 + int(prob/15)  # 1-186
            start = interval - t  
        else:
            it_list = [14,27,39,50,60,69,77,84,90,95,99,102,104,105]
            prob -= 15*(max_cd-14)    #[0,105)
            for i in range(14):
                if prob < it_list[i]:
                    t = max_cd - 14 +1 +i  # 187-200
                    interval = randint(max_cd -14 +i +1,max_cd)
                    start = interval - t
                    break
        # end fix

        if always:  # 动曾
            for i in hit:
                if start<i:    # start__0__start+74___start+158，需要严格小于
                    tmp[i-start] = dmg
        while True:
            interval = randint(max_cd-14,max_cd)  # 186-200
            if t + interval>=M:  
                break
            for i in hit:
                tmp[t+i] = dmg  # 相应命中时间赋值
            t += interval  # 更新下一个t
        return tmp

def test_dmg():
    # 生成植物
    plt :list[IO] = []
    for p in plant_list:
        plt.append(IO(p[0]))  # 每个植物都有对应时间点伤害

    hp = 300  # 15豌豆
    t_eat = randint(350,353)
    ans = 0

    for i in range(M):
        for p in plt:
            if p.list[i-p.start]!=0:
                hp -= p.list[i-p.start]
        if hp<=0:
            return ans
        if i>=t_eat and (i-t_eat) % 4 == 0: #啃食最后结算
            ans += 4
    print('excel')

def my_tst(N):
    ans = np.array(np.zeros(150))  #不会超过600hp
    tmp = 1
    for i in range(N):
        res = test_dmg()
        ans[res//4] += 1
        if i == round(N*(tmp/100)) :
            ht_count = np.dot(ans[1:],np.array(np.ones(149)))
            ht_hp = np.dot(ans,np.array(range(150))*4)
            print(f"process:{100*i/N:.2f}%  count:{100*ht_count/(i+1):.5f}%  hp:{ht_hp/(i+1):.5f}")
            tmp += 1

    ht_count = np.dot(ans[1:],np.array(np.ones(149)))
    ht_hp = np.dot(ans,np.array(range(150))*4)
    print(f"mean dmg:{ht_hp/N:.5f}  mean count:{ht_count/N:.5f}")
    
    # 作图
    max_idx = np.nonzero(ans)[0][-1]
    x = np.array(range(max_idx+1)) * 4
    plt.figure(figsize=(20, 10))
    plt.bar(x,ans[0:max_idx+1])
    plt.yscale('log')
    plt.title(f"mean dmg:{ht_hp/N:.5f} dmg prob:{ht_count/N:.5f}")
    plt.xlabel('dmg')
    plt.ylabel('frequency')
    plt.show()

my_tst(test_N)