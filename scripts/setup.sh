#!/bin/bash
# usage from the terminal in the same location as the setup.sh run './setup.sh'

# color variables
GREEN=$(tput setaf 2)
NORMAL=$(tput sgr0)

# create directories {code, data, models, notebooks, pipeline}
printf "${GREEN}Creating folder structure${NORMAL}\n\n"
mkdir {code,data,models,notebooks,pipeline} 2>&1 >/dev/null
mkdir data/{attributes,raw} 2>&1 >/dev/null

# create __init__.py in code dir
printf "${GREEN}Creating __init.py in code dir${NORMAL}\n\n"
touch code/__init__.py

# install requirements.txt packages
printf "${GREEN}Install requirements.txt${NORMAL}\n\n"
pip install -r requirements.txt 2>&1 >/dev/null

# cleanup notebook checkpoint files that cause errors "RuntimeError: Files in same split /* have different header."
printf "${GREEN}Cleanup notebook checkpoint files in data directories.${NORMAL}\n\n"
rm -rf data/{new,raw}/.ipynb_checkpoints 2>&1 >/dev/null

