# mkdir F:\PHA_data\P38945
import os
import pandas as pd
from biopandas.pdb import PandasPdb
import requests
import csv
import sys

# root_path="F:/PHA_data/4hbd/structural_domain"
# mkdir_root_path="F:\\PHA_data\\4hbd\\structural_domain"
# tsv_path="F:/PHA_data/4hbd/structural_domain/structure-matching-PF00465.tsv"

# root_path="F:/PHA_data/P38945/PF00465"
# mkdir_root_path="F:\\PHA_data\\P38945\\PF00465"
# tsv_path="F:/PHA_data/P38945/PF00465/structure-matching-PF00465.tsv"


# root_path="F:/PHA_data/4hbd_change_list"
# mkdir_root_path="F:\\PHA_data\\4hbd_change_list"
# tsv_path="F:/PHA_data/4hbd_change_list/structure-matching-PF00465.tsv"

# root_path="F:/PHA_data/orfz_PDB_outfile2"
# mkdir_root_path="F:\\PHA_data\\orfz_PDB_outfile2"
# tsv_path="F:/PHA_data/orfz_PDB_outfile2/structure-matching-PF00465.tsv"

# root_path="F:/PHA_data/orfz_PDB_outfile2/false"
# # mkdir_root_path="F:\\PHA_data\\orfz_PDB_outfile2\\false"
# # tsv_path="F:/PHA_data/orfz_PDB_outfile2/false/structure-matching-PF00465.tsv"

# root_path="F:/PHA_data/orfz_PDB_outfile2/a"
# mkdir_root_path="F:\\PHA_data\\orfz_PDB_outfile2\\a"
# tsv_path="F:/PHA_data/orfz_PDB_outfile2/a/structure-matching-PF00465.tsv"

# root_path="F:/PHA_data/orfz_PDB_outfile3"
# mkdir_root_path="F:\\PHA_data\\orfz_PDB_outfile3"
# tsv_path="F:/PHA_data/orfz_PDB_outfile3/structure-matching-PF00465.tsv"

# root_path="F:/PHA_data/pf13336_nature"
# mkdir_root_path="F:\\PHA_data\\pf13336_nature"
# tsv_path="F:/PHA_data/pf13336_nature/structure-matching-PF13336.tsv"

# root_path="F:/PHA_data/orfz_and_4eu8"
# mkdir_root_path="F:\\PHA_data\\orfz_and_4eu8"
# tsv_path="F:/PHA_data/orfz_and_4eu8"

root_path=sys.argv[1]
structural_domain_pdb_path_path=sys.argv[2]
mgltools_path=sys.argv[3]
vina_path=sys.argv[4]
ligand_path_one=sys.argv[5]
if len(sys.argv) >= 7:  # 检查是否提供了足够的参数（包括脚本名称在内）
    ligand_path_two = sys.argv[6]
else:
    ligand_path_two = ""
mkdir_root_path=root_path
tsv_path=root_path

def main(root_path,mkdir_root_path,tsv_path,structural_domain_pdb_path_path,mgltools_path,vina_path,ligand_path_one,ligand_path_two):
    # pdb_down(tsv_path,mkdir_root_path)
    # structural_domain_split(tsv_path,root_path,mkdir_root_path)
    os.chmod(root_path, 0o777)
    os.chmod(root_path, 0o777)
    os.chmod(vina_path, 0o777)
    Batch_process_receptor(root_path,mkdir_root_path,structural_domain_pdb_path_path,mgltools_path)
    Batch_multiple_docking(root_path,mkdir_root_path,structural_domain_pdb_path_path,vina_path,ligand_path_one,ligand_path_two)
    docking_score_to_tsv(root_path)

    # file="93.txt"
    # vague_path = root_path + "/docking_result" + "/" + file[:-3] + "pdbqt"
    # out = root_path + "/docking_txt_two" + "/" + file
    # out_path_true_path = root_path + "/docking_result_two" + "/" + file[:-3] + "pdbqt"
    # process_structural_domain_pdb = root_path + "/process_structural_domain_pdb" + "/" + file[:-3] + "pdbqt"
    #
    # os.system("mkdir " + mkdir_root_path + "\\docking_txt_two")
    # os.system("mkdir " + mkdir_root_path + "\\docking_result_two")
    #
    # Batch_multiple_docking_two(vague_path,out,out_path_true_path,process_structural_domain_pdb)

def pdb_down(tsv_path,mkdir_root_path):
    data = pd.read_table(tsv_path,sep='\t')
    pdb_ids = data['Accession'].str.upper()
    headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82'
    }
    base_url = 'https://files.rcsb.org/download/'
    file_format = '.pdb'

    os.system("mkdir "+mkdir_root_path+"/pdb")
    os.chmod(mkdir_root_path+"/pdb", 0o777)
    for pdb_id in pdb_ids:
        try:
            res = requests.get(base_url+pdb_id+file_format)
            if res.status_code == 200:
                with open(mkdir_root_path+"/pdb/"+pdb_id+file_format, "wb") as f:
                    f.write(res.content)
        except Exception as e:

            print(e)

def structural_domain_split(tsv_path,root_path,mkdir_root_path):
    domains = pd.read_table(tsv_path)[['Accession', 'matches']]
    # print(domains)
    domains['start_end'] = domains['matches'].apply(lambda x: x.split(";")[0])
    filter_domains = domains[['Accession', 'start_end']]


    # 对人工指导的需要，对自然酶则不用
    str_array = [str(num) for num in filter_domains['Accession']]
    filter_domains['Accession']=str_array

    os.system("mkdir " + mkdir_root_path + "/structural_domain_pdb")
    os.chmod(mkdir_root_path + "/structural_domain_pdb", 0o777)
    

    # 读取本地的pdb文件
    files = filter(lambda x: x.endswith("pdb"), os.listdir(root_path + "/pdb"))
    new_name = 'structural_domain_'
    for domain_file in files:
        protein_name = domain_file[0:-4].lower()
        # print(filter_domains['Accession'])
        # print(protein_name)
        position = filter_domains.loc[filter_domains['Accession'] == protein_name, 'start_end']
        # print(filter_domains['Accession'] == protein_name)
        # print()
        # print("wow")
        if len(position) > 0:
            # print("wow")
            start = int(position.iloc[0].split("..")[0])
            end = int(position.iloc[0].split("..")[1])
            data = PandasPdb().read_pdb(os.path.join(root_path + "/pdb", domain_file))
            data.to_pdb(os.path.join(root_path +"/structural_domain_pdb", new_name + domain_file))
            atom_df = data.df['ATOM']
            hetatm_df = data.df['HETATM']
            new_atom_df = atom_df.loc[(atom_df['residue_number'] >= start) & (atom_df['residue_number'] <= end)]
            new_hetatm_df = hetatm_df.loc[(hetatm_df['residue_number'] >= start) & (hetatm_df['residue_number'] <= end)]
            data._df['ATOM'] = new_atom_df
            data._df['HETATM'] = new_hetatm_df
            data.to_pdb(os.path.join(root_path +"/structural_domain_pdb", new_name + domain_file), append_newline=True)

def Batch_process_receptor(root_path,mkdir_root_path,structural_domain_pdb_path_path,mgltools_path):
    structural_domain_pdb_path=structural_domain_pdb_path_path
    out_path=root_path+"/process_structural_domain_pdb"

    os.system("mkdir " + mkdir_root_path + "/process_structural_domain_pdb")
    os.chmod(mkdir_root_path + "/process_structural_domain_pdb", 0o777)

    for root, dirs, files in os.walk(structural_domain_pdb_path):
        for file in files:
            pdb_file = structural_domain_pdb_path + "/" + file
            output_file = out_path + "/" + file + "qt"
            print(pdb_file)

            os.system(
                mgltools_path+"/bin/pythonsh "+mgltools_path+"/MGLToolsPckgs/AutoDockTools/Utilities24/prepare_receptor4.py -r " + pdb_file + " -o " + output_file + " -A checkhydrogens")

            if os.path.exists(output_file):
                number_process(output_file)

def Batch_multiple_docking(root_path,mkdir_root_path,structural_domain_pdb_path_path,vina_path,ligand_path_one,ligand_path_two):

    os.system("mkdir " + mkdir_root_path + "/docking_txt")
    #os.system("mkdir " + mkdir_root_path + "/docking_txt_two")
    os.system("mkdir " + mkdir_root_path + "/docking_result")
    #os.system("mkdir " + mkdir_root_path + "/docking_result_two")

    for root, dirs, files in os.walk(root_path+"/process_structural_domain_pdb"):
        for file in files:
            path = root + "/" + file
            out = root_path+"/docking_txt" + "/" + file
            out = out[:-5]
            out = out + "txt"
            out_path_true_path = root_path+"/docking_result" + "/" + file
            # out_path_true_path = out_path_true_path[:-2]
            
            pocketminer_file_path = root_path + "/pocketminer_txt/" +file[:-2] +".txt" 
            structural_pdb = structural_domain_pdb_path_path + "/" +file[:-2]
            center_x, center_y, center_z, size_x, size_y, size_z=Searching_for_sites_from_PocketMiner(pocketminer_file_path,structural_pdb)
            
            file = open(out, 'w')
            file.write("receptor = " + path + "\n")
            file.write("ligand = "+ligand_path_one+"\n")
            if ligand_path_two!="":
                file.write("ligand = "+ligand_path_two+"\n")
            file.write("center_x = "+str(center_x)+"\n")
            file.write("center_y = "+str(center_y)+"\n")
            file.write("center_z = "+str(center_z)+"\n")
            file.write("size_x = " + str((size_x )) + "\n")
            file.write("size_y = " + str((size_y )) + "\n")
            file.write("size_z = " + str((size_z )) + "\n")
            file.write("exhaustiveness = 8\n")
            file.write("out = " + out_path_true_path + "\n")
            

            
            
    for root, dirs, files in os.walk(root_path+"/docking_txt"):
        for file in files:
            path = root_path+"/docking_txt" + "/" + file
            os.system(vina_path+" --config " + path)

            #vague_path = root_path + "/docking_result" + "/" + file[:-3]+"pdbqt"
            #out = root_path+"/docking_txt_two" + "/" + file
            #out_path_true_path=root_path+"/docking_result_two" + "/" + file[:-3]+"pdbqt"
            #process_structural_domain_pdb=root_path+"/process_structural_domain_pdb" + "/" + file[:-3]+"pdbqt"
            #Batch_multiple_docking_two(vague_path,out,out_path_true_path,process_structural_domain_pdb)

def Batch_multiple_docking_two(vague_path,out,out_path_true_path,process_structural_domain_pdb):
    print(vague_path,out,out_path_true_path,process_structural_domain_pdb)


    center_x, center_y, center_z, size_x, size_y, size_z=get_docking_box(vague_path)
    print(center_x, center_y, center_z, size_x, size_y, size_z)

    file = open(out, 'w')
    file.write("receptor = " + process_structural_domain_pdb + "\n")
    file.write("ligand = /mnt/galE/substrate/UDP_a_D_glucose.pdbqt\n")
    #file.write("ligand = /mnt/neuA/substrate/N_acylneuraminate.pdbqt\n")
    file.write("center_x = "+str(center_x)+"\n")
    file.write("center_y = "+str(center_y)+"\n")
    file.write("center_z = "+str(center_z)+"\n")
    file.write("size_x = " + str((size_x + 10)) + "\n")
    file.write("size_y = " + str((size_y + 10)) + "\n")
    file.write("size_z = " + str((size_z + 10)) + "\n")
    file.write("exhaustiveness = 32\n")
    file.write("out = " + out_path_true_path + "\n")
    file.close()

    os.system("/mnt/docking/vina_1.2.3/vina_1.2.5_linux_x86_64 --config " + out)



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

    return center_x, center_y, center_z, size_x, size_y, size_z

def docking_score_to_tsv(root_path):
    file = root_path+"/docking_result"
    path_csv_file =root_path +"/Structural_Domain_Multiple_Docking.csv"
    with open(path_csv_file, mode='w', newline='') as fi:
        writer = csv.writer(fi)
        writer.writerow(['Name of enzyme', 'X', 'Y', 'Z', 'Score'])

    for root, dirs, files in os.walk(file):
        for file in files:
            path = root + "/" + file
            print(path)
            index = file.index(".")
            result = file[:index]

            coordinates, scores = extract_coordinates_and_scores(path)
            save_to_csv(path_csv_file, result, coordinates, scores)


def extract_coordinates_and_scores(pdb_file):
    coordinates = []
    scores = []

    with open(pdb_file, 'r') as f:
        lines = f.readlines()

    x = ""
    y = ""
    z = ""

    for line in lines:
        if line.startswith("HETATM"):
            elements = line.split()
            x = x + elements[6] + ";"
            y = y + elements[7] + ";"
            z = z + elements[8] + ";"

        elif line.startswith("REMARK VINA RESULT:"):
            elements = line.split()
            score = float(elements[3])
            scores.append(score)
        if line.startswith("ENDMDL"):
            break
    coordinates.append((x, y, z))
    return coordinates, scores

def save_to_csv(filename, result, coordinates, scores):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        for i in range(len(coordinates)):
            x, y, z = coordinates[i]
            score = scores[i]
            writer.writerow([result, x, y, z, score])

def number_process(filename):

    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)  # 将文件指针移回文件开头
        modified_line_one = ""
        modified_line_two = ""
        modified_line_three = ""
        modified_line_four = ""
        modified_line_five = ""

        for line in lines:
            if len(line) >= 34 and line[33] == " ":  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line = line[:33] + line[34:]  # 删除第五个字符
            else:
                modified_line = line  # 如果行长度小于5，不进行修改，保留原始行内容

            if len(modified_line) >= 39 and modified_line[38] != " " and modified_line[38] != "-":  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_one = modified_line[:32] + modified_line[33:39] + " " + modified_line[39:]  # 删除第五个字符
            elif len(modified_line) >= 39 and modified_line[38] != " " and modified_line[38] == "-":
                modified_line_one = modified_line[:32] + modified_line[33:38]+ " " + modified_line[38:]
            elif len(modified_line) >= 39 and modified_line[37] != " " and modified_line[37] == "-":
                modified_line_one = modified_line[:32] + modified_line[33:37] + "  " + modified_line[37:]
            else:
                modified_line_one = modified_line  # 如果行长度小于5，不进行修改，保留原始行内容

            modified_line=modified_line_one

            if len(modified_line) >= 39 and modified_line[37] ==" ":
                modified_line_one = modified_line[:37] + "0" + modified_line[38:]

            if len(modified_line_one) >= 41 and modified_line_one[40] == " ":  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_two = modified_line_one[:40] + modified_line_one[41:]  # 删除第五个字符
            else:
                modified_line_two = modified_line_one  # 如果行长度小于5，不进行修改，保留原始行内容

            modified_line = modified_line_two

            if len(modified_line) >= 40 and modified_line[39] == " ":  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_two = modified_line[:39] + modified_line[40:]  # 删除第五个字符
            else:
                modified_line_two = modified_line  # 如果行长度小于5，不进行修改，保留原始行内容
            #
            if len(modified_line_two) >= 48 and modified_line_two[44] == "-" :  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_three = modified_line_two[:44] + " " + modified_line_two[44:]
                if len(modified_line_three) >= 48 and modified_line_three[45] == "-" :  # 只有在至少有5个字符的情况下才删除第五个字符
                    modified_line_three = modified_line_three[:45] + " " + modified_line_three[45:]
            elif len(modified_line_two) >= 48 and modified_line_two[45] == "-" :  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_three = modified_line_two[:45] + " " + modified_line_two[45:]
            elif len(modified_line_two) >= 48 and modified_line_two[46] != " " :  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_three = modified_line_two[:46] + " " + modified_line_two[46:]
            elif len(modified_line_two) >= 48 and modified_line_two[47] != " " :  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_three = modified_line_two[:47] + " " + modified_line_two[47:]
            # elif len(modified_line_two) >= 48 and modified_line_two[47] == "-":
            #     modified_line_three = modified_line_two[:46] + " " + modified_line_two[46:] # 删除第五个字符
            else:
                modified_line_three = modified_line_two  # 如果行长度小于5，不进行修改，保留原始行内容

            if len(modified_line_three) >= 46 and modified_line_three[45] == " ":  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_four = modified_line_three[:45] + "0" + modified_line_three[46:]  # 删除第五个字符
            else:
                modified_line_four = modified_line_three  # 如果行长度小于5，不进行修改，保留原始行内容

            modified_line = modified_line_four

            if len(modified_line) >= 45 and modified_line[44] == " ":  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_four = modified_line[:44] + "0" + modified_line[45:]  # 删除第五个字符
            else:
                modified_line_four = modified_line  # 如果行长度小于5，不进行修改，保留原始行内容

            if len(modified_line_four) >= 54 and modified_line_four[53] == " ":  # 只有在至少有5个字符的情况下才删除第五个字符
                modified_line_five = modified_line_four[:53] + "0" + modified_line_four[53:]  # 删除第五个字符
            else:
                modified_line_five = modified_line_four  # 如果行长度小于5，不进行修改，保留原始行内容


            file.write(modified_line_five)

        file.truncate()  # 删除文件剩余部分（可根据需要决定是否保留该行）
        
def Searching_for_sites_from_PocketMiner(txt_path,pdb_path):
    print(txt_path)
    with open(txt_path, 'r') as f:
        lines = f.readlines()

    x_min = 200
    y_min = 200
    z_min = 200
    x_max = 0
    y_max = 0
    z_max = 0

    x_atom = []
    y_atom = []
    z_atom = []



    #filtered_lines = [line for line in lines if float(line) > 0.9]
    filtered_lines = [int(index) for index, line in enumerate(lines) if float(line) > 0.8]
    print(filtered_lines)
    
    with open(pdb_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if line.startswith("ATOM"):
            elements = line.split()
            #print(elements[5])
            if int(elements[5]) in filtered_lines:
                #print("true")
                x_atom.append(float(elements[6]))
                y_atom.append(float(elements[7]))
                z_atom.append(float(elements[8]))


    for i in range(len(x_atom)):
        if (x_atom[i] < x_min):
            x_min = float(x_atom[i])
        if (x_atom[i] > x_max):
            x_max = float(x_atom[i])
        if (y_atom[i] < y_min):
            y_min = float(y_atom[i])
        if (y_atom[i] > y_max):
            y_max = float(y_atom[i])
        if (z_atom[i] < z_min):
            z_min = float(z_atom[i])
        if (z_atom[i] > z_max):
            z_max = float(z_atom[i])

    center_x = round((x_min + x_max) / 2, 3)
    center_y = round((y_min + y_max) / 2, 3)
    center_z = round((z_min + z_max) / 2, 3)
    size_x = round(x_max - x_min, 3)
    size_y = round(y_max - y_min, 3)
    size_z = round(z_max - z_min, 3)

    return center_x, center_y,center_z,size_x+10,size_y+10,size_z+10

main(root_path,mkdir_root_path,tsv_path,structural_domain_pdb_path_path,mgltools_path,vina_path,ligand_path_one,ligand_path_two)