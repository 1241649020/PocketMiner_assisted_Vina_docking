import os
def Searching_for_sites_from_PUResNetV2(result_path):
    with open(result_path, 'r') as f:
        lines = f.readlines()

    x_min = 200
    y_min = 200
    z_min = 200
    x_max = -200
    y_max = -200
    z_max = -200
    
    
    for line in lines:
        elements = line.split()
        if (float(elements[6]) < x_min):
            x_min = float(elements[6])
        if (float(elements[6]) > x_max):
            x_max = float(elements[6])
        if (float(elements[7]) < y_min):
            y_min = float(elements[7])
        if (float(elements[7]) > y_max):
            y_max = float(elements[7])
        if (float(elements[8]) < z_min):
            z_min = float(elements[8])
        if (float(elements[8]) > z_max):
            z_max = float(elements[8])
    
    center_x = round((x_min + x_max) / 2, 3)
    center_y = round((y_min + y_max) / 2, 3)
    center_z = round((z_min + z_max) / 2, 3)
    size_x = round(x_max - x_min, 3)
    size_y = round(y_max - y_min, 3)
    size_z = round(z_max - z_min, 3)
    
    x_min=x_min-5
    y_min=y_min-5
    
    z_min=z_min-5
    x_max=x_max+5
    y_max=y_max+5
    z_max=z_max+5

    return x_min, y_min,z_min,x_max,y_max,z_max

def get_docking_box(pdb_file):

    with open(pdb_file, 'r') as f:
        lines = f.readlines()

    x_min = 200
    y_min = 200
    z_min = 200
    x_max = -200
    y_max = -200
    z_max = -200

    for line in lines:
        if line.startswith("HETATM"):
            elements = line.split()
            if (float(elements[5]) < x_min):
                x_min = float(elements[5])
            if (float(elements[5]) > x_max):
                x_max = float(elements[5])
            if (float(elements[6]) < y_min):
                y_min = float(elements[6])
            if (float(elements[6]) > y_max):
                y_max = float(elements[6])
            if (float(elements[7]) < z_min):
                z_min = float(elements[7])
            if (float(elements[7]) > z_max):
                z_max = float(elements[7])
        if line.startswith("ENDMDL"):
            break

    center_x = round((x_min + x_max) / 2, 3)
    center_y = round((y_min + y_max) / 2, 3)
    center_z = round((z_min + z_max) / 2, 3)
    size_x = round(x_max - x_min, 3)
    size_y = round(y_max - y_min, 3)
    size_z = round(z_max - z_min, 3)

    return x_min, y_min,z_min,x_max,y_max,z_max

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

puresnetv2_file_path="/mnt/PUResNetV2/results"
structural_pdb="/mnt/galE/structural_domain_pdb"
result_pdb="/mnt/galE/docking_result"

sum=0
ture_num=0
for root, dirs, files in os.walk(structural_pdb):
        for file in files:
            if len(file)>14 and file[-14:]=="checkpoint.pdb" :
                continue
            structural_file = structural_pdb + "/" + file
            puresnetv2_file = puresnetv2_file_path + "/" + file[:-4] +"/" +"0_A_"+file
            result_file = result_pdb + "/" + file +"qt"
            
            if not os.path.exists(puresnetv2_file):
                sum=sum+1
                continue
            

            puresnetv2_x_min, puresnetv2_y_min,puresnetv2_z_min,puresnetv2_x_max,puresnetv2_y_max,puresnetv2_z_max=Searching_for_sites_from_PUResNetV2(puresnetv2_file)
            
            docking_box_x_min, docking_box_y_min,docking_box_z_min,docking_box_x_max,docking_box_y_max,docking_box_z_max=get_docking_box(result_file)
            
            ratio_1, ratio_2 = calculate_ratio(puresnetv2_x_min, puresnetv2_x_max, puresnetv2_y_min, puresnetv2_y_max, puresnetv2_z_min, puresnetv2_z_max, docking_box_x_min, docking_box_x_max, docking_box_y_min, docking_box_y_max, docking_box_z_min, docking_box_z_max)
            print(file)
            print("实验对接盒子除交叉部分外自身的体积占总体积的比例:", ratio_1)
            print("参照对接盒子除交叉部分外自身的体积占总体积的比例:", ratio_2)
            sum=sum+1
            if ratio_2<0.10:
                ture_num=ture_num+1
                
print(ture_num/sum)