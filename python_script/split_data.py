from dpdata import MultiSystems, LabeledSystem
import os
import numpy as np

# 定义主文件夹路径
main_folder = '/personal/B_Al_Ga_In_N/AlN/'

try:
    # 使用 from_dir 方法结合通配符读取所有 OUTCAR 文件
    vasp_multi_systems = MultiSystems.from_dir(
        dir_name=main_folder,
        file_name="*/OUTCAR",
        fmt="vasp/outcar"
    )

    # 打印多体系信息
    print(vasp_multi_systems)
    print(vasp_multi_systems.systems)

    # 将 MultiSystems 中的所有数据合并为一个 LabeledSystem 对象
    all_data = LabeledSystem()
    for system in vasp_multi_systems.systems.values():
        all_data.append(system)

    # 数据总帧数
    total_frames = len(all_data)

    # 计算测试集的帧数，按 8:2 的比例划分
    test_size = int(total_frames * 0.2)

    # 随机选择测试集的索引
    index_test = np.random.choice(total_frames, size=test_size, replace=False)

    # 其他索引作为训练集数据
    index_training = list(set(range(total_frames)) - set(index_test))

    # 提取训练集和测试集数据
    data_training = all_data.sub_system(index_training)
    data_test = all_data.sub_system(index_test)

    # 定义训练集和测试集的输出文件夹
    training_output_dir = '/personal/B_Al_Ga_In_N/AlN/training_data'
    test_output_dir = '/personal/B_Al_Ga_In_N/AlN/test_data'

    # 检查训练集输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(training_output_dir):
        os.makedirs(training_output_dir)

    # 检查测试集输出文件夹是否存在，如果不存在则创建
    if not os.path.exists(test_output_dir):
        os.makedirs(test_output_dir)

    # 将训练集数据导出为 DeepMD npy 格式
    data_training.to_deepmd_npy(training_output_dir)

    # 将测试集数据导出为 DeepMD npy 格式
    data_test.to_deepmd_npy(test_output_dir)

    print(f"训练数据已成功导出到 {training_output_dir} 文件夹，包含 {len(data_training)} 帧。")
    print(f"测试数据已成功导出到 {test_output_dir} 文件夹，包含 {len(data_test)} 帧。")

except Exception as e:
    print(f"处理过程中出现错误: {e}")
