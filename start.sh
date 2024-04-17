#!/usr/bin/zsh
sudo apt-get update
sudo apt install python3-pip
pip3 install git+https://github.com/NVIDIA/NeMo.git
pip3 install hydra-core --upgrade
pip3 install pytorch_lightning
pip3 install librosa
pip3 install sentencepiece
pip3 install pandas
pip3 install inflect
pip3 install lhotse
pip3 install editdistance
pip3 install jiwer
pip3 install pyannote.core
pip3 install webdataset
pip3 install datasets
pip3 install pyannote.metrics
pip3 install IPython
sudo touch ./output.log
sudo chmod 777 ./output.log
sudo chmod 733 ./server.py
sudo nohup python3 ./server.py > ./output.log &
