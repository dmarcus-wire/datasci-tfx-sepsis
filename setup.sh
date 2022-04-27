#!/bin/bash
# usage from the terminal in the same location as the setup.sh run './setup.sh'

# color variables
GREEN=$(tput setaf 2)
NORMAL=$(tput sgr0)

# create directories {code, data, models, notebooks, pipeline}
printf "${GREEN}Creating folder structure${NORMAL}\n\n"
mkdir {code,data,models,notebooks,pipeline}
mkdir data/{attributes,raw}

# create __init__.py in code dir
printf "${GREEN}Creating __init.py in code dir${NORMAL}\n\n"
touch code/__init__.py

# install requirements.txt packages
printf "${GREEN}Install requirements.txt${NORMAL}\n\n"
pip install -r requirements.txt