import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import os

def read_phonopy_branches(file_path, method_name):
    """读取带分支（空行分隔）的phonopy数据，返回分支数据和高对称点"""
    branches = []
    current_branch = []
    high_symmetry_points = []
    reading_high_points = False
    
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:  # 空行，结束当前分支
                if current_branch:
                    branches.append(current_branch)
                    current_branch = []
                continue
                
            if line.startswith('#'):
                # 处理高对称点注释（支持多行）
                if "End points of segments" in line:
                    reading_high_points = True
                    # 尝试从当前行提取数据
                    parts = line.split(':')
                    if len(parts) > 1:
                        points_str = parts[1].strip()
                        if points_str:
                            high_symmetry_points.extend([float(p) for p in points_str.split()])
                    continue
                
                if reading_high_points and line.startswith('#'):
                    # 继续从后续注释行提取数据
                    points_str = line.lstrip('#').strip()
                    if points_str:
                        high_symmetry_points.extend([float(p) for p in points_str.split()])
                    continue
                else:
                    reading_high_points = False
            
            # 解析数据行（q, freq）
            try:
                q, freq = map(float, line.split())
                current_branch.append([q, freq])
            except:
                pass  # 忽略无效行
                
        # 处理最后一个分支
        if current_branch:
            branches.append(current_branch)
    
    # 转换为DataFrame，每个分支带索引
    df_list = []
    for branch_idx, branch in enumerate(branches):
        df = pd.DataFrame(branch, columns=['q', 'freq'])
        df['method'] = method_name
        df['branch'] = branch_idx  # 分支编号（0,1,2,...）
        df_list.append(df)
    return pd.concat(df_list, ignore_index=True), high_symmetry_points

def plot_phonon_branches(files, output="phonon_branches.png", dpi=600):
    """绘制多方法多分支声子谱"""
    plt.figure(figsize=(12, 8))
    ax = plt.gca()
    
   

    method_colors = {
    'DFT': '#a50f15',   # 深红色
    'DP': '#084594'  # 深蓝色
    }
    
    # 线条样式配置（按方法区分）
    method_linestyles = {
        'DFT': '-',    # 实线
        'DP': '--'    # 虚线
    }
    
    # 读取第一个方法的数据以获取高对称点（假设所有方法路径相同）
    first_method = next(iter(files))
    first_file = files[first_method]
    if not os.path.exists(first_file):
        print(f"错误：找不到第一个方法的文件 {first_file}")
        return
    
    first_df, first_high_points = read_phonopy_branches(first_file, first_method)
    
    # 打印提取的高对称点（用于调试）
    print(f"从 {first_method} 文件中提取的高对称点: {first_high_points}")
    
    # 定义高对称点标签（根据您的计算路径修改）
    high_symmetry_labels = ['Γ', 'M', 'K', 'Γ']
    
    # 确保标签数量与高对称点数量匹配
    if len(high_symmetry_labels) != len(first_high_points):
        print(f"警告：高对称点标签数量({len(high_symmetry_labels)})与实际点数({len(first_high_points)})不匹配")
        high_symmetry_labels = high_symmetry_labels[:len(first_high_points)]  # 截断标签列表
    
    # 绘制所有方法的数据
    for method, file in files.items():
        if not os.path.exists(file):
            print(f"跳过：找不到文件 {file}")
            continue
            
        df, _ = read_phonopy_branches(file, method)  # 忽略此方法的高对称点（使用第一个方法的）
        
        # 按分支绘制每个方法的数据
        for branch_idx in df['branch'].unique():
            branch_df = df[df['branch'] == branch_idx]
            ax.plot(
                branch_df['q'], branch_df['freq'],
                color=method_colors[method],
                linestyle=method_linestyles[method],
                linewidth=2,
                label=f"{method}" if branch_idx == 0 else None  # 仅为每个方法的第一个分支添加标签
            )
    
    # 设置高对称点位置和标签
    ax.set_xticks(first_high_points)
    #ax.set_xticklabels(high_symmetry_labels)
    ax.set_xticklabels(high_symmetry_labels, 
                   fontsize=28,         # 设置字体大小
                   fontname='Times New Roman')  # 设置字体

    
    # 在高对称点位置添加垂直线
    for point in first_high_points:
        ax.axvline(x=point, color='gray', linestyle='--', alpha=0.5)
    
    # 美化设置
    #ax.set_xlabel('Wave Vector', fontsize=14)
    ax.set_ylabel('Frequency (THz)', fontsize=28, fontname='Times New Roman')


    # 设置Y轴刻度标签及其样式
    ax.set_yticklabels(ax.get_yticks(),  # 使用当前Y轴刻度值
                   fontsize=28,       # 设置字体大小
                   fontname='Times New Roman')  # 设置字体

    #ax.set_title('Phonon Dispersion Comparison', fontsize=16, fontname='Times New Roman')
    ax.grid(alpha=0.3, linestyle='--')
    
    # 设置图例和坐标轴范围
    ax.legend(prop={'family': 'Times New Roman', 'size': 24},  loc='upper right')
    ax.yaxis.set_minor_locator(MultipleLocator(1))  # 次要刻度
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    
    # 设置Y轴范围（确保包含零）
    all_data = pd.concat([read_phonopy_branches(file, method)[0] for method, file in files.items()])
    y_min = min(0, all_data['freq'].min() * 1.1)
    y_max = all_data['freq'].max() * 1.2
    ax.set_ylim(y_min, y_max)
    
    plt.tight_layout()
    plt.savefig(output, dpi=dpi, bbox_inches='tight')
    plt.show()

# 主程序：指定文件路径
if __name__ == "__main__":
    method_files = {
        'DFT': r'F:\2D_dp\2D_dp\picture\phono_picture\phono_2\InN\phonon_vasp.out',
        'DP': r'F:\2D_dp\2D_dp\picture\phono_picture\phono_2\InN\phonon1.out'
    }
    
    plot_phonon_branches(method_files, 
                         output=r"F:\2D_dp\2D_dp\picture\phono_picture\phono_2\InN\InNbranched_phonon222.png")