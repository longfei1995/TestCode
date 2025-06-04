import numpy as np
import pandas as pd
from sklearn.datasets import make_classification

def generate_lane_dataset(n_samples=1000, random_state=42):
    """
    生成车道分类的模拟数据集
    
    Parameters:
    n_samples: 样本数量
    random_state: 随机种子
    
    Returns:
    X: 特征矩阵
    y: 标签向量 (1: 在本车道, 0: 不在本车道)
    """
    np.random.seed(random_state)
    
    # 创建空的特征数组
    features = []
    labels = []
    
    # 生成在车道内的样本 (约70%的数据)
    n_in_lane = int(n_samples * 0.7)
    for _ in range(n_in_lane):
        # 在车道内的车辆特征
        lateral_offset = np.random.normal(0, 0.3)  # 横向偏移较小，均值为0
        heading_angle = np.random.normal(0, 5)     # 航向角较小，单位：度
        lane_center_dist = np.abs(np.random.normal(0, 0.5))  # 到车道中心距离较小
        width_ratio = np.random.uniform(0.3, 0.8)  # 车宽比例合理
        
        features.append([lateral_offset, heading_angle, lane_center_dist, width_ratio])
        labels.append(1)  # 在本车道
    
    # 生成不在车道内的样本 (约30%的数据)
    n_out_lane = n_samples - n_in_lane
    for _ in range(n_out_lane):
        # 不在车道内的车辆特征
        lateral_offset = np.random.choice([-1, 1]) * np.random.uniform(1.5, 3.0)  # 横向偏移较大
        heading_angle = np.random.normal(0, 15)    # 航向角可能较大
        lane_center_dist = np.random.uniform(1.5, 4.0)  # 到车道中心距离较大
        width_ratio = np.random.uniform(0.2, 1.0)  # 车宽比例变化范围大
        
        features.append([lateral_offset, heading_angle, lane_center_dist, width_ratio])
        labels.append(0)  # 不在本车道
    
    # 转换为numpy数组
    X = np.array(features)
    y = np.array(labels)
    
    # 打乱数据顺序
    indices = np.random.permutation(len(X))
    X = X[indices]
    y = y[indices]
    
    return X, y

def generate_vehicle_data_dict(features):
    """
    将特征数组转换为字典格式，适配extract_features方法
    """
    vehicle_data = {
        'lateral_offset': features[0],
        'heading_angle': features[1], 
        'lane_center_distance': features[2],
        'vehicle_width': features[3] * 3.5,  # 假设车道宽度为3.5米
        'lane_width': 3.5
    }
    return vehicle_data

if __name__ == "__main__":
    # 生成数据集
    X, y = generate_lane_dataset(n_samples=1000)
    
    print("数据集信息:")
    print(f"总样本数: {len(X)}")
    print(f"在车道内样本数: {np.sum(y == 1)}")
    print(f"不在车道内样本数: {np.sum(y == 0)}")
    print(f"特征维度: {X.shape[1]}")
    print("\n特征统计:")
    feature_names = ['lateral_offset', 'heading_angle', 'lane_center_distance', 'width_ratio']
    for i, name in enumerate(feature_names):
        print(f"{name}: 均值={X[:, i].mean():.3f}, 标准差={X[:, i].std():.3f}") 