#!/bin/bash

mgltools_path="/usr/local/MGLTools-1.5.7/mgltools_x86_64Linux2_1.5.7"
vina_path="/home/xccc/docking/vina_1.2.5_linux_x86_64"
xtal_predict_path="/home/xccc/gvp-pocket_pred/src/xtal_predict.py"
PocketMiner_docking_path="/home/xccc/Full_process_script/PocketMiner_docking.py"
python_path="/root/miniconda3/envs/pocketminer/bin/python"

root=$1
structural_domain_pdb_path_path=$2
ligand_path_one=$3
ligand_path_two=$4


$python_path  $xtal_predict_path $root $structural_domain_pdb_path_path

$python_path  $PocketMiner_docking_path  $root $structural_domain_pdb_path_path $mgltools_path $vina_path $ligand_path_one $ligand_path_twowhich