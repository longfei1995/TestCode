import numpy as np
import random
import os
from matplotlib import pyplot as plt




if __name__ == "__main__":
    # 画1000个随机的gauss分布的点
    x = list(range(1000))
    y = [random.uniform(0, 1) for _ in range(1000)]
    
    plt.figure(figsize=(10, 6))  # 创建图形并设置大小
    plt.scatter(x, y)  # 一次性绘制所有点
    plt.title("高斯分布随机点")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)  # 添加网格
    plt.show()