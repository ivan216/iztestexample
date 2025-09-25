import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import nbinom, skewnorm, gamma, skew
from skewnorm import fit_skewnormal
from fit_gamma import fit_gamma

def plot_qq_nbinom(counts_array, ifplot = True):
    # 将counts_array转换为原始数据数组
    data = []
    for value, count in enumerate(counts_array):
        data.extend([value] * int(count))
    data = np.array(data)
    
    mean = np.mean(data)
    vari = np.var(data,ddof=1)
    r = mean**2/(mean+vari)
    p = mean/(mean+vari)
    
    if ifplot:
        # 实际数据的分位数
        sorted_data = np.sort(data)
        n_obs = len(sorted_data)
        empirical_quantiles = np.arange(1, n_obs + 1) / (n_obs + 1)  # 概率点
        
        # 理论分布的分位数
        theoretical_quantiles = nbinom.ppf(empirical_quantiles, r, p, loc=r)
        min_val = min(sorted_data.min(), theoretical_quantiles.min())
        max_val = max(sorted_data.max(), theoretical_quantiles.max())

        # 绘制QQ图
        plt.figure()
        plt.scatter(theoretical_quantiles, sorted_data)
        plt.plot([min_val, max_val], [min_val, max_val], 'r--')
        plt.title("Q-Q: simulate vs nbinom")
        plt.xlabel("nbin")
        plt.ylabel("simulate")
        plt.grid(True, linestyle='--')

    return r, p

def plot_qq_skewnorm(counts_array, ifplot = True):
    data = []
    for value, count in enumerate(counts_array):
        data.extend([value] * int(count))
    data = np.array(data)
    
    mean = np.mean(data)
    vari = np.var(data,ddof=1)
    skewness = skew(data)
    ksi, omega, alpha = fit_skewnormal(mean, vari, skewness)

    if ifplot:
        sorted_data = np.sort(data)
        n_obs = len(sorted_data)
        empirical_quantiles = np.arange(1, n_obs + 1) / (n_obs + 1)  # 概率点

        theoretical_quantiles = skewnorm.ppf(empirical_quantiles, alpha, loc=ksi, scale=omega)
        min_val = min(sorted_data.min(), theoretical_quantiles.min())
        max_val = max(sorted_data.max(), theoretical_quantiles.max())

        plt.figure()
        plt.scatter(theoretical_quantiles, sorted_data)
        plt.plot([min_val, max_val], [min_val, max_val], 'r--')
        plt.title("Q-Q: simulate vs skewnorm")
        plt.xlabel("skewnorm")
        plt.ylabel("simulate")
        plt.grid(True, linestyle='--')
    
    return ksi, omega, alpha


def plot_qq_gamma(counts_array, ifplot=True):
    data = []
    for value, count in enumerate(counts_array):
        data.extend([value] * int(count))
    data = np.array(data)

    mean = np.mean(data)
    vari = np.var(data,ddof=1)
    skewness = skew(data)

    alpha, beta, c = fit_gamma(mean, vari, skewness)

    if ifplot:
        sorted_data = np.sort(data)
        n_obs = len(sorted_data)
        empirical_quantiles = np.arange(1, n_obs + 1) / (n_obs + 1)  # 概率点

        theoretical_quantiles = gamma.ppf(empirical_quantiles, alpha, loc=c, scale=1/beta)
        min_val = min(sorted_data.min(), theoretical_quantiles.min())
        max_val = max(sorted_data.max(), theoretical_quantiles.max())     

        plt.figure()
        plt.scatter(theoretical_quantiles, sorted_data)
        plt.plot([min_val, max_val], [min_val, max_val], 'r--')
        plt.title("Q-Q: simulate vs gamma")
        plt.xlabel("gamma")
        plt.ylabel("simulate")
        plt.grid(True, linestyle='--')
    
    return alpha, beta, c


# 示例用法
if __name__ == "__main__":
    # 模拟数据（下标代表数值，元素值代表个数）
    true_n, true_p = 5, 0.3
    sample = nbinom.rvs(true_n, true_p, loc=true_n, size=100000)
    max_val = sample.max()
    counts_array = np.zeros(max_val + 1, dtype=int)
    for val in sample:
        counts_array[val] += 1
    
    # 绘制QQ图
    n, p = plot_qq_nbinom(counts_array)
    
    print(f"真实参数: n={true_n}, p={true_p}")
    print(f"拟合参数: n={n:.4f}, p={p:.4f}")

    plt.show()
    