import tensorflow as tf
from models import MQAModel
import numpy as np
from glob import glob
import mdtraj as md
import os
import sys

from validate_performance_on_xtals import process_strucs, predict_on_xtals

def make_predictions(pdb_paths, model, nn_path, debug=False, output_basename=None):
    '''
        pdb_paths : list of pdb paths
        model : MQAModel corresponding to network in nn_path
        nn_path : path to checkpoint files
    '''
    strucs = [md.load(s) for s in pdb_paths]
    X, S, mask = process_strucs(strucs)
    if debug:
        np.save(f'{output_basename}_X.npy', X)
        np.save(f'{output_basename}_S.npy', S)
        np.save(f'{output_basename}_mask.npy', mask)
    predictions = predict_on_xtals(model, nn_path, X, S, mask)
    return predictions

# main method
if __name__ == '__main__':
    fi=sys.argv[1]
    file = sys.argv[2]
    output_folder =fi+'/pocketminer_txt'
    os.system("mkdir " + output_folder)
    # TO DO - provide input pdb(s), output name, and output folder
    for root, dirs, files in os.walk(file):
        for file in files:
            path = root + "/" + file
            strucs = [
                path,
            ]
            output_name = file
            
            
            
            print()
            print()
            print()
            print()
            print()
            print(file)
            print()
            print()
            print()
            print()
            print()
            

            # debugging mode can be turned on to output protein features and sequence
            debug = False

            # Load MQA Model used for selected NN network
            nn_path = "/home/xccc/gvp-pocket_pred/models/pocketminer"
            DROPOUT_RATE = 0.1
            NUM_LAYERS = 4
            HIDDEN_DIM = 100
            model = MQAModel(node_features=(8, 50), edge_features=(1, 32),
                             hidden_dim=(16, HIDDEN_DIM),
                             num_layers=NUM_LAYERS, dropout=DROPOUT_RATE)


            if debug:
                output_basename = f'{output_folder}/{output_name}'
                
                predictions = make_predictions(strucs, model, nn_path, debug=True, output_basename=output_basename)
            else:
                predictions = make_predictions(strucs, model, nn_path)

            # output filename can be modified here
            np.save(f'{output_folder}/{output_name}.npy', predictions)
            np.savetxt(os.path.join(output_folder,f'{output_name}.txt'), predictions, fmt='%.4g', delimiter='\n')


