#!/bin/bash
# usage from the terminal in the same location as the cleanup.sh run './cleanup.sh'

printf "${GREEN}Delete folders {code,data,models,pipeline}${NORMAL}\n\n"
rm -rf {code,data,models,pipeline}