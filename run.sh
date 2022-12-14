#!/usr/bin/bash

# set up virtual environment
sudo apt-get install python3-venv
python3.9 -m venv nlp-env
source ./nlp-env/bin/activate

# prettier outputs
GREEN='\033[1;32m'
NC='\033[0m'
# update apt-get
sudo apt-get update
# this assumes python3.9 - change if different
sudo apt-get install python3.9-dev -y

# creating the virtual environment
#pip install virtualenv
#virtualenv -p /usr/bin/python3.9 nlp-env
# activate the environment
#source nlp-env/bin/activate

pip install --upgrade pip
pip install bertopic
# install packages
pip install fasttext-wheel

# done
echo -e "[${GREEN}INFO:${NC}] Everything installed!"

