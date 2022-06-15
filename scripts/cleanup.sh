#!/bin/bash
# usage from the terminal in the same location as the cleanup.sh run './cleanup.sh'

printf "${GREEN}Delete folders {code,data,models,pipeline}${NORMAL}\n\n"
rm -rf {code,data,models,pipeline}

# install requirements.txt packages
printf "${GREEN}Uninstall requirements.txt${NORMAL}\n\n"
pip install -r requirements.txt