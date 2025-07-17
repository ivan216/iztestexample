import scipy.stats as stats

def ci_fun(x_mean = 0.5,alpha = 0.05,n = 10000):
    ## x_mean 测得过率 ## alpha 置信水平 ## n 测试次数 
    quantile = stats.norm.ppf(1-alpha/2,loc=0,scale=1)
    # quantile = 1.96
    a = n + quantile**2
    b = -2*n*x_mean - quantile**2
    c = n * x_mean**2
    p1 = (-b - (b**2 - 4*a*c)**(1/2) )/2/a
    p2 = (-b + (b**2 - 4*a*c)**(1/2) )/2/a

    print(f"测试次数 {n}, 测得过率 {x_mean}, 置信水平为 {1-alpha} 的置信区间为:")
    print(f"({p1:e}, {p2:e})")
    return [p1,p2]

ci_fun(0.000149,0.05,int(1e7))
