Supporting environment:

Ubuntu 20.04


Getting started / installation


1. Deploy the PocketMiner environment and the running environment of this project

from https://github.com/Mickdub/gvp Pull the project from the middle and create a new requirements. txt file in the main directory, with the following content filled in:

Numpy=1.18.1

Scipy==1.4.1

Pandas=1.0.3

Tensorflow=2.1.0

Tqdm==4.42.1

Mdtraj

Run the following commands line by line in the command line:

Conda create - n pocketminer Python==3.7.6

Conda activate pocket miner

#CD -->requirements. txt directory

Pip install - r requirements. txt

Conda install - c Conda forge protobuf

Conda install pyyaml

Pip install biopandas

Replace the xtal_predict. py file in the original PocketMiner project with the xtal_predict. py file in the repository.


2. Install Autodock Tools and Autodock Vina

Download Autodock Tools and install Autodock Vina from the official website.

PS: After downloading version 1.2.3 of Autodock Vina, because the new version of Autodock Vina supports multiple docking, this software can call its kernel for multiple docking. However, if you don't need 

multiple docking, it doesn't matter.


3. Pull this project and change the configuration

After pulling this project to the local location, modify the settings in PocketMiner'full_process.sh as follows:

Change mgltools.path to the address of Autodock Tools.

Change vina_path to the address of the Autodock Vina kernel.

Change xtal_predict_path to the address of the xtal_predict.py file in PocketMiner.

Change the address of the cost project PocketMineer_docking. py to PocketMineer_docking. py.

Change Python path to the address of Python in the Pocketminer environment.

Example:

Mgltools path="/usr/local/MGLTools 1.5.7/mgltools x86_64Linux2 1.5.7"

Vina_path="/home/xccc/docking/vina_1.2.5_linux_x86_64"

Xtal_predict_path="/home/xccc/gvp pocket_pred/src/xtal_predict. py"

PocketMineer_docking path="/home/xccc/Full_process_script/PacketMineer_docking. py"

Python path="/root/miniconda3/envs/pocketminer/bin/Python"


4. Operation

Run the command line in the main directory of this project/ You can open the UI interface by clicking on PocketMiner-assisted_Vina_docking_UI or by double clicking on PocketMiner-assisted_Vina_docking_UI. 

Then, simply follow the instructions provided.


PS: If you don't need a graphical user interface and want to operate directly from the command line, you can run PocketMiner'full_processs.sh and input: output address, enzyme protein folder address, and 

small molecule address.
