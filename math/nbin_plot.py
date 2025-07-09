import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import nbinom
from scipy.special import gamma,gammaln

## 用连续的函数进行拟合
def nbin_entend_to_real(x,r,p):
    x = 1.0*x
    # 用对数gamma处理 防溢出
    ln_res = np.piecewise(x,[x<r],[0,lambda x: gammaln(x) + (x-r)*np.log(1-p) - gammaln(x-r+1) +  r*np.log(p) - gammaln(r)])
    res = np.piecewise(ln_res, [ln_res==0], [0, lambda x: np.exp(x)])
    return res

r = 10
p = 0.4
x_plot = np.arange(0, 70)
# alpha = r*(1-p)
# beta = p
# g_pdf = gamma.pdf(x_plot, alpha, scale = 1/beta, loc=round(r))
n_pmf = nbinom.pmf(x_plot, r, p, loc = round(r))
nr_pmf = nbin_entend_to_real(x_plot,r,p)
# plt.plot(x_plot,g_pdf,color='r')
plt.plot(x_plot,nr_pmf,color='g')
plt.bar(x_plot,n_pmf)
plt.show()


## 直接进行离散拟合
# p = 0.3395
# r = 10.9076
##real tt 765.0
# r = 10.5473
# p = 0.3286
# x = 65
# res = nbinom.cdf(x, r, p, loc = round(r))
# print(res)


## 尾巴处的结果
# p = 0.3416
# r = 10.5480
# res = 0.0
# # x = 150
# x = 300
# for i in range(20):
#     res += nbinom.pmf(x+i, r, p, loc = round(r))
# print(res)
