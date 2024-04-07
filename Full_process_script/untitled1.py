def calculate_volume(x1, x2, y1, y2, z1, z2):
    # 计算立方体的体积
    volume = (x2 - x1) * (y2 - y1) * (z2 - z1)
    return volume

def calculate_overlap_volume(x1, x2, y1, y2, z1, z2, x1_, x2_, y1_, y2_, z1_, z2_):
    # 计算交叉部分的体积
    overlap_x = max(0, min(x2, x2_) - max(x1, x1_))
    overlap_y = max(0, min(y2, y2_) - max(y1, y1_))
    overlap_z = max(0, min(z2, z2_) - max(z1, z1_))
    overlap_volume = overlap_x * overlap_y * overlap_z
    return overlap_volume

def calculate_ratio(x1, x2, y1, y2, z1, z2, x1_, x2_, y1_, y2_, z1_, z2_):
    # 计算每个立方体的体积
    volume_1 = calculate_volume(x1, x2, y1, y2, z1, z2)
    volume_2 = calculate_volume(x1_, x2_, y1_, y2_, z1_, z2_)
    
    # 计算交叉部分的体积
    overlap_volume = calculate_overlap_volume(x1, x2, y1, y2, z1, z2, x1_, x2_, y1_, y2_, z1_, z2_)
    
    # 计算除交叉部分外自身的体积
    self_volume_1 = volume_1 - overlap_volume
    self_volume_2 = volume_2 - overlap_volume
    
    # 计算占比
    ratio_1 = self_volume_1 / volume_1
    ratio_2 = self_volume_2 / volume_2
    
    return ratio_1, ratio_2

# 示例坐标值
x1, x2 = 0, 5
y1, y2 = 0, 5
z1, z2 = 0, 5

x1_, x2_ = 2, 7
y1_, y2_ = 2, 7
z1_, z2_ = 2, 7

# 计算比例
ratio_1, ratio_2 = calculate_ratio(x1, x2, y1, y2, z1, z2, x1_, x2_, y1_, y2_, z1_, z2_)
print("第一个立方体除交叉部分外自身的体积占总体积的比例:", ratio_1)
print("第二个立方体除交叉部分外自身的体积占总体积的比例:", ratio_2)