#!/bin/bash
IFS=$'\n'
if [[ ${1} = '' || ${1} = '-h' || ${1} = '--help' ]];then
    echo "Usage: $0 <First_name> <Last_name>"
    echo ""
    exit
else
    name="$1 $2"
    export $name 2>/dev/null
    source /home/${USER}/scripts/Python/ADAddUser/bin/activate
    python /home/${USER}/scripts/Python/ADAddUser/ADadduser.py -g ${name}
    deactivate
fi

