import scipy.stats as stats
import numpy as np

def ci_fun(x_mean = 0.5,alpha = 0.05,n = 10000):
    ## x_mean 测得过率 ## alpha 置信水平 ## n 测试次数 
    quantile = stats.norm.ppf(1-alpha/2,loc=0,scale=1)
    # quantile = 1.96
    a = n + quantile**2
    b = -2*n*x_mean - quantile**2
    c = n * x_mean**2
    p1 = (-b - (b**2 - 4*a*c)**(1/2) )/2/a
    p2 = (-b + (b**2 - 4*a*c)**(1/2) )/2/a
    return np.array([p1,p2])

# print("测试次数",n,",测得过率",x_mean,",置信水平为",1-alpha,"的置信区间为：")
# print("(",'%.4f'%inf,",",'%.4f'%sup,")")

##2023智商杯图十，全部补75
##得到的期望 相应的置信区间
# result = 225+175+225+150+150+75*(ci_fun(0.1)+ci_fun(0.16)+ci_fun(0.04)
#                                  +ci_fun(0.43)+ci_fun(0.61))

result = ci_fun(0.0001,0.05,10000)
print(result)
