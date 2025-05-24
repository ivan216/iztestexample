import scipy.stats as stats
import numpy as np

n = 1000    #每行测试次数 64500
alpha = 0.05    # 1-alpha 置信水平
wi = np.array([75,75,75,75,75]) #每行补刀花费
xi = 1 - np.array([0.9,0.84,0.96,0.57,0.39])
# 1 - 每行测得成功率 = 每行测得失败率

quantile = stats.norm.ppf(1-alpha/2,loc=0,scale=1)

sample_sum = np.dot(xi, wi)
width2 = np.sqrt( np.dot(wi**2,xi*(1-xi))/(n) ) * quantile
inf2 = sample_sum - width2
sup2 = sample_sum + width2

print(f"经验公式估计 ( {inf2:.4f}, {sup2:.4f} )")
