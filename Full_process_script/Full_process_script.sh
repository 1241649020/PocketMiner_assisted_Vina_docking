#!/bin/bash

root="/mnt/zhong_ke_yuan_ce_shi_jiyin_three/tubian_one"

RFdiffusion="/mnt/RFdiffusion"

inference_input_pdb="$root/RFdiffusion_input_pdb/zhong_ke_yuan_ce_shi_jiyin.pdb"

RFdiffusion_out="$root/RFdiffusion_output_pdb"

contigmap_contigs="[A1-55/1-1/A57-69/10-10/A80-121/8-8/A130-208/1-1/A210-229/5-5/A235-338/21-21/A360-378/1-1/A380-393]"

inference_num_designs=300

ProteinMPNN="/mnt/ProteinMPNN/ProteinMPNN-main/examples"

ProteinMPNN_input_dir="$root/ProteinMPNN_input"

ProteinMPNN_output_dir="$root/ProteinMPNN_output"

ProteinMPNN_path_for_parsed_chains="$ProteinMPNN_output_dir/parsed_pdbs.jsonl"



# source activate myconda

# cd $RFdiffusion

# if [ ! -d $RFdiffusion_out ]
# then
#    mkdir -p $RFdiffusion_out
# fi

# python ./scripts/run_inference.py inference.input_pdb=$inference_input_pdb "contigmap.contigs=$contigmap_contigs" inference.output_prefix="$RFdiffusion_out/" inference.num_designs=$inference_num_designs inference.ckpt_override_path="$RFdiffusion/models/ActiveSite_ckpt.pt"

# source activate mlfold

# if [ ! -d $ProteinMPNN_input_dir ]
# then
#    mkdir -p $ProteinMPNN_input_dir
# fi

# if [ ! -d $ProteinMPNN_output_dir ]
# then
#    mkdir -p $ProteinMPNN_output_dir
# fi


# cd $ProteinMPNN

# for file in "$RFdiffusion_out"/*; do
#    if [[ -f "$file" && "$file" == *".pdb" ]]; then
#        cp $file $ProteinMPNN_input_dir
#    fi
# done


# python ../helper_scripts/parse_multiple_chains.py --input_path=$ProteinMPNN_input_dir --output_path=$ProteinMPNN_path_for_parsed_chains

# python ../protein_mpnn_run.py \
#         --jsonl_path $ProteinMPNN_path_for_parsed_chains \
#         --out_folder $ProteinMPNN_output_dir \
#         --num_seq_per_target 100 \
#         --sampling_temp "0.1" \
#         --seed 37 \
#         --batch_size 1


python /mnt/hydrophilicity/sele_hy.py $root

# source activate esm

# python /mnt/Full_process_script/fa_to_pdb.py $root

#source activate myconda

# python /mnt/docking/Full_process_docking_Searching_for_sites.py