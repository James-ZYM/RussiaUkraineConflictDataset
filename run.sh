#!/usr/bin/bash
# prettier outputs
GREEN='\033[1;32m'
NC='\033[0m'
# update apt-get
sudo apt-get update
# this assumes python3.9 - change if different
sudo apt-get install python3.9-dev -y
# upgrade pip; install BERTopic
pip install --upgrade pip
pip install bertopic
# done
echo -e "[${GREEN}INFO:${NC}] Everything installed!"

#in terminal write: bash NLP\ examproject\ \(293386\)/NLPexam/run.sh
