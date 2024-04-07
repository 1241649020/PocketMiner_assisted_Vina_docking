import csv
import os
file = "/home/xcc/galE/structural_domain_pdb"
path_csv_file ="/home/xcc/galE/Structural_Domain_Multiple_Docking.csv"
with open(path_csv_file, mode='w', newline='') as fi:
    writer = csv.writer(fi)
    writer.writerow(['complex_name', 'protein_path', 'ligand_description', 'protein_sequence'])

for root, dirs, files in os.walk(file):
    for file in files:
        if len(file) > 14 and file[-14:] == "checkpoint.pdb":
            continue
        path = root + "/" + file
        print(path)
        index = file.index(".")
        result = file[:index]

        with open(path_csv_file, mode='a', newline='') as fi:
            writer = csv.writer(fi)
            writer.writerow([result, path, "/home/xcc/galE/substrate/UDP-a-D-glucose.sdf", ""])
