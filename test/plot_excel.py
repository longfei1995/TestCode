import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D  # 添加这行导入

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
plt.rcParams['axes.unicode_minus'] = False    # 正确显示负号

# 读取CSV文件
def load_data(file_path):
    df = pd.read_csv(file_path)
    # 将价格列转换为数值型
    df['价格'] = df['价格(YB)'].apply(lambda x: float(x.replace('w', '')) * 10000 if isinstance(x, str) else x)
    return df

# 为不同的属性组合绘制图表
def plot_attribute_combinations(df):
    # 获取所有可能的属性列
    attribute_cols = ['属性', '会心', '增伤', '命中', '力量', '灵气', '体力', '定力', '身法']
    
    # 按种类分组
    for kind, group in df.groupby('种类'):
        # 查找该种类装备中存在的属性组合
        existing_combinations = []
        
        for _, row in group.iterrows():
            # 找出当前行中非空的属性
            present_attrs = []
            for attr in attribute_cols:
                # 当前行中哪些属性有值(既不是 NaN 也不是 0)
                if pd.notna(row[attr]) and row[attr] != 0:
                    present_attrs.append(attr)
            
            if len(present_attrs) >= 2:
                # 对每种属性组合绘制图表
                combo_key = '+'.join(present_attrs)
                
                if combo_key not in existing_combinations:
                    existing_combinations.append(combo_key)
                    
                    # 筛选具有这些属性的数据
                    combo_data = group.copy()
                    for attr in attribute_cols:
                        if attr not in present_attrs:
                            combo_data = combo_data[pd.isna(combo_data[attr]) | (combo_data[attr] == 0)]
                    
                    # 如果有足够的数据点，则绘制图表
                    if len(combo_data) > 0:
                        create_plot_for_combination(kind, combo_data, present_attrs)

# 为特定属性组合创建图表
def create_plot_for_combination(kind, data, attributes):
    # 对于两个属性的情况
    if len(attributes) == 2:
        attr1, attr2 = attributes
        plt.figure(figsize=(8, 6))
        scatter = plt.scatter(data[attr1], data[attr2], c=data['价格']/10000, 
                              s=100, cmap='cividis')
        
        for i, row in data.iterrows():
            plt.annotate(f"{row['价格']/10000:.1f}w", 
                         (row[attr1], row[attr2]),
                         xytext=(5, 5), textcoords='offset points')
        
        plt.colorbar(scatter, label='价格(万)')
        plt.title(f'{kind} - {attr1}+{attr2}与价格关系')
        plt.xlabel(f'{attr1}数值')
        plt.ylabel(f'{attr2}数值')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.savefig(f'{kind}:{attr1}+{attr2}_价格关系.png')
        plt.close()
    
    # 对于三个属性的情况，使用二维气泡图
    elif len(attributes) == 3:
        pass
        

# 主函数
def main():
    file_path = 'test/ling_wu.csv'
    df = load_data(file_path)
    
    # 数据检查
    print("数据概览:")
    print(df.head())
    
    # 绘制不同属性组合的图表
    plot_attribute_combinations(df)
    
    print("分析完成！图表已保存。")

if __name__ == "__main__":
    main()
