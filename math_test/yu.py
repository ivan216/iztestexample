import numpy as np

n = 5  # 玉米数量
cnt = 10**7  # 大概投掷次数
t_list = np.array([15*i for i in range(1,287)]+[4290+15*i-(i+1)*i//2 for i in range(1,15)])
t_length = 293.0*cnt  # 截取时间长度

def corns(n,cnt):
    '''
    计算 停滞倍率 = 总时间/(总时间 - 停滞时间)
    '''
    t_rand = np.random.randint(1,4396,(n,1))
    t = np.searchsorted(t_list, t_rand) # 0-299 初次攻击分布

    c1 = np.random.randint(286,301,(n,cnt-1)).astype(float)
    c1 = np.concatenate((t,c1),axis=1)
    c1 = np.cumsum(c1,axis=1)
    
    ## 若某个植物攻击总时间未到设定时间，进行补充
    last_col = c1[:,-1].reshape(n,-1)
    fix_mat = np.zeros((n,0))
    while np.any(last_col < t_length):
        ran_col = np.random.randint(286,301,(n,1))
        last_col += ran_col
        fix_mat = np.concatenate((fix_mat,last_col),axis=1)
    
    c1 = np.concatenate((c1,fix_mat), axis=1)
    c2 = np.random.rand(*np.shape(c1)) > 0.75

    y = c1[c2]  # 黄油对应时机
    y = y[y<t_length]  # 舍弃超过设定时间的部分
    y = np.sort(y)  # 排序好的黄油命中时机

    stag = 0.0  # 计算停滞时间
    diff = y[1:] - y[:-1]
    stag += 400 * np.sum(diff >= 400).astype(float)  # 相差超过400, 只增加400
    stag += np.sum(diff[diff<400])  # 相差小于400, 增加差值
    stag += min(t_length-y[-1],400) # 最后一发黄油的停滞

    return t_length / (t_length - stag)

print("running...")
res = corns(n,cnt)
print(res)
