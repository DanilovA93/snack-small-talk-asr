#!/usr/bin/zsh
sudo apt-get update
sudo apt install python3-pip
pip3 install -r requirements.txt
pip3 install git+https://github.com/NVIDIA/NeMo.git
pip3 install hydra-core --upgrade
touch ./output.log
chmod 777 ./output.log
chmod 733 ./server.py
nohup python3 ./server.py > ./output.log &
