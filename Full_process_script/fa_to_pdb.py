import os
import subprocess
import sys
import esm
import torch



def sequences_to_pdb(input_filename, output_folder):
    # 读取输入文件中的序列
    with open(input_filename, 'r') as input_file:
        lines = input_file.readlines()

    sequences = []
    current_sequence = ''
    current_name = ''
    current_range = ''
    line_number = 0
    for line in lines:
        line_number=line_number+1
        if(line_number % 2 == 0):
            sequences.append(line.strip())


    # 定义 Curl 命令的基础部分
    #curl_base_command = 'curl -X POST --data'

    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    sum=0
    for sequence in sequences:
        #print(sequence)
        sum+=1
        # 构建 Curl 命令
        #curl_command = f'{curl_base_command} "{sequence}" https://api.esmatlas.com/foldSequence/v1/pdb/'

        # 运行 Curl 命令并捕获输出
        #result = subprocess.run(curl_command, capture_output=True, text=True, shell=True)
        #print(result)
        
        with torch.no_grad():
            result = model.infer_pdb(sequence)

        # 检查返回代码
        #if result.returncode == 0:
        if True:
            #pdb_content = result.stdout
            pdb_content = result
            print((f'{input_filename[:-6]+"_"+str(sum)}.pdb').split('/')[-1])
            pdb_filename = os.path.join(output_folder, (f'{os.path.basename(input_filename)[:-6]+"_"+str(sum)}.pdb').split('/')[-1])
            with open(pdb_filename, 'w') as pdb_file:
                pdb_file.write(pdb_content)
            #test(pdb_filename,sequence,sum,input_filename,output_folder)
            print(f"Sequence {pdb_filename} converted to PDB format and saved to {pdb_filename}")
        else:
            pdb_filename = os.path.join(output_folder, (f'{os.path.basename(input_filename)[:-6]+"_"+str(sum)}.pdb').split('/')[-1])
            print(f"Error converting sequence {pdb_filename} to PDB format:")

def test(pdb_filename,sequence,sum,input_filename,output_folder):
    with open(pdb_filename, 'r') as file:
        lines = file.readlines()
        if len(lines) < 3:
            curl_base_command = 'curl -X POST --data'
            curl_command = f'{curl_base_command} "{sequence}" https://api.esmatlas.com/foldSequence/v1/pdb/'

            # 运行 Curl 命令并捕获输出
            result = subprocess.run(curl_command, capture_output=True, text=True, shell=True)

            # 检查返回代码
            if result.returncode == 0:
                pdb_content = result.stdout
                print( (f'{input_filename[:-6]+"_"+str(sum)}.pdb').split('/')[-1])
                pdb_filename = os.path.join(output_folder,  (f'{os.path.basename(input_filename)[:-6]+"_"+str(sum)}.pdb').split('/')[-1])
                with open(pdb_filename, 'w') as pdb_file:
                    pdb_file.write(pdb_content)
                test(pdb_filename, sequence, sum,input_filename,output_folder)
    return



model = esm.pretrained.esmfold_v1()
model = model.eval().cuda()

ro = sys.argv[1]
print(ro)
#pdb_path=root+"/ProteinMPNN_output"
#fasta_path=root+"/fasta_output"
#pdb_to_fasta(pdb_path,fasta_path)
for root, dirs, files in os.walk(ro+"/ProteinMPNN_output/seqs"):
    for file in files:
        path = root + "/" + file
        if path[-6:]==".fasta":
            if path[-16:]=="checkpoint.fasta":
                continue
            print(ro+"/Artificial_guidance_for_optimizing_enzymes")
            sequences_to_pdb(path,ro+"/Artificial_guidance_for_optimizing_enzymes")