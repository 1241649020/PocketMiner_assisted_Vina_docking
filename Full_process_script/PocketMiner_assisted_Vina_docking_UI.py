import tkinter as tk
from tkinter import filedialog
import subprocess

def use_shell():
    # 定义要执行的Shell脚本路径
    script_path = './PocketMiner_full_process.sh'

    env_name = "pocketminer"

    if label_root["text"]=="" or label_root["text"]=="output folder address":
        label_txt.config(anchor="center",font=("Arial", 12),fg="red",text="The output folder address has not been entered yet")
    elif label_structural_domain_pdb_path_path["text"]=="" or label_structural_domain_pdb_path_path["text"]=="enzyme protein folder address":
        label_txt.config(anchor="center",font=("Arial", 12),fg="red",text="The enzyme protein folder address has not been entered yet")
    elif label_ligand_path_one["text"]=="" or label_ligand_path_one["text"]=="the first small molecule address":
        label_txt.config(anchor="center",font=("Arial", 12),fg="red",text="The first small molecule address has not been entered yet")
    else:
        if label_ligand_path_two["text"]=="" or label_ligand_path_two["text"]=="the second small molecule address(No need to choose for single docking)":
            args = [label_root["text"],label_structural_domain_pdb_path_path["text"],label_ligand_path_one["text"]]
        else:
            args = [label_root["text"], label_structural_domain_pdb_path_path["text"], label_ligand_path_one["text"],label_ligand_path_two["text"]]

        print("Working!!!")
        label_txt.config(anchor="center", font=("Arial", 12), fg="yellow", text="Working")
        label_txt.update()
        # 使用subprocess模块调用Shell脚本
        try:
            # subprocess.run(['conda', 'activate', "pocketminer"], shell=True, check=True)
            process=subprocess.run(['conda', 'run', '-n', env_name, 'bash', script_path] + args, check=True)
            label_txt.config(anchor="center", font=("Arial", 12), fg="green", text="Done")
            print("Shell脚本执行成功！")
        except subprocess.CalledProcessError as e:
            print("Shell脚本执行失败:", e)


def select_root_folder():
    # 打开文件夹选择对话框
    folder_path = filedialog.askdirectory()

    # 更新标签文本为所选文件夹的名称
    label_root.config(text=folder_path)

def select_structural_domain_pdb_path_path_folder():
    # 打开文件夹选择对话框
    folder_path = filedialog.askdirectory()

    # 更新标签文本为所选文件夹的名称
    label_structural_domain_pdb_path_path.config(text=folder_path)

def select_ligand_path_one_folder():
    # 打开文件夹选择对话框
    folder_path = filedialog.askopenfilename()

    # 更新标签文本为所选文件夹的名称
    label_ligand_path_one.config(text=folder_path)

def select_ligand_path_two_folder():
    # 打开文件夹选择对话框
    folder_path = filedialog.askopenfilename()

    # 更新标签文本为所选文件夹的名称
    label_ligand_path_two.config(text=folder_path)


root = tk.Tk()
root.geometry("500x500")
root.title("PocketMiner_assisted_Vina_docking")
#root.configure(bg="white")




label = tk.Label(root, wraplength=480,text="This program is used to assist in enzyme protein molecule docking. Please enter the output address, enzyme protein folder address, small molecule address (enter one small molecule address for single docking, two small molecule addresses for multiple docking), and press the start button to start the program docking.")
label.place(x=10,y=20)

label_root = tk.Label(root, text="output folder address",bg='white',anchor="center")
label_root.config(anchor="center",font=("Arial", 10))
label_root.place(y=315,width=500)


button_root = tk.Button(root, text="Select output folder address", command=select_root_folder)
button_root.config(anchor="center",font=("Arial", 10))
button_root.place(x=135,y=280)


label_structural_domain_pdb_path_path = tk.Label(root, text="enzyme protein folder address", bg='white',anchor="center")
label_structural_domain_pdb_path_path.config(anchor="center",font=("Arial", 10))
label_structural_domain_pdb_path_path.place(y=135,width=500)


button_structural_domain_pdb_path_path = tk.Button(root, text="Select enzyme protein folder address", command=select_structural_domain_pdb_path_path_folder)
button_structural_domain_pdb_path_path.config(anchor="center",font=("Arial", 10))
button_structural_domain_pdb_path_path.place(x=115,y=100)

label_ligand_path_one = tk.Label(root, text="the first small molecule address",bg='white',anchor="center")
label_ligand_path_one.config(anchor="center",font=("Arial", 10))
label_ligand_path_one.place(y=195,width=500)


button_ligand_path_one = tk.Button(root, text="Select the first small molecule address", command=select_ligand_path_one_folder)
button_ligand_path_one.config(anchor="center",font=("Arial", 10))
button_ligand_path_one.place(x=102,y=160)

label_ligand_path_two = tk.Label(root,text="the second small molecule address(No need to choose for single docking)",bg='white',anchor="center")
label_ligand_path_two.config(anchor="center",font=("Arial", 10))
label_ligand_path_two.place(y=255,width=500)


button_ligand_path_two = tk.Button(root, text="Select the second small molecule address", command=select_ligand_path_two_folder)
button_ligand_path_two.config(anchor="center",font=("Arial", 10))
button_ligand_path_two.place(x=100,y=220)

button_working = tk.Button(root, text="Working", command=use_shell)
button_working.config(anchor="center",font=("Arial", 20))
button_working.place(x=180,y=350)

label_txt = tk.Label(root,wraplength=480,text="",anchor="center")
label_txt.config(anchor="center",font=("Arial", 12))
label_txt.place(y=400,width=500)


root.mainloop()


