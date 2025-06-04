import numpy as np
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from data_set import generate_lane_dataset  # 导入数据生成函数

class LaneClassificationSVM:
    def __init__(self):
        self.model = SVC(kernel='rbf', C=1.0, gamma='scale')
        self.scaler = StandardScaler()
        
    def extract_features(self, vehicle_data):
        """提取手工特征"""
        features = []
        # 横向位置特征
        lateral_offset = vehicle_data['lateral_offset']
        # 航向角特征  
        heading_angle = vehicle_data['heading_angle']
        # 到车道中心距离
        lane_center_dist = vehicle_data['lane_center_distance']
        # 车道宽度比例
        width_ratio = vehicle_data['vehicle_width'] / vehicle_data['lane_width']
        
        features = [lateral_offset, heading_angle, lane_center_dist, width_ratio]
        return np.array(features)
    
    def train(self, X_train, y_train):
        """训练SVM模型"""
        # 特征标准化
        X_train_scaled = self.scaler.fit_transform(X_train)
        # 训练模型
        self.model.fit(X_train_scaled, y_train)
        
    def predict(self, X_test):
        """预测车辆是否在本车道"""
        X_test_scaled = self.scaler.transform(X_test)
        return self.model.predict(X_test_scaled)

# 使用示例
def main():
    # 1. 加载数据集
    print("正在生成模拟数据集...")
    X, y = generate_lane_dataset(n_samples=1000, random_state=42)
    print(f"数据集生成完成: {X.shape[0]}个样本, {X.shape[1]}个特征")
    
    # 2. 划分训练/测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"训练集大小: {X_train.shape[0]}")
    print(f"测试集大小: {X_test.shape[0]}")
    
    # 3. 训练模型
    classifier = LaneClassificationSVM()
    classifier.train(X_train, y_train)
    print("模型训练完成")
    
    # 4. 预测和评估
    y_pred = classifier.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"分类准确率: {accuracy:.3f}")
    print("\n详细分类报告:")
    print(classification_report(y_test, y_pred, target_names=['不在车道', '在车道']))

if __name__ == "__main__":
    main()
 