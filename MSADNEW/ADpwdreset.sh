#!/bin/bash
if [[ ${1} = "" || ${1} = "-h" || ${1} = "--help" ]];then
    echo -ne "\nUsage: ${0} <AD_login_id>\n\n"
    exit
fi

export loginid=${1}

# Modify the path to the python virtual environment if it is not saved in
# your home directory under MSADNEW
source /home/${USER}/MSADNEW/bin/activate 
python /home/${USER}/MSADNEW/ADpasswdResetNEW.py -u ${loginid}
deactivate
exit 0
