#!/bin/bash
if [[ ${1} = "" || ${1} = "-h" || ${1} = "--help" ]];then
    echo -ne "\nUsage: ${0} <AD_login_id>\n\n"
    exit
fi

export loginid=${1}
source /home/jlickey/scripts/Python/MSADNEW/bin/activate 
python /home/jlickey/scripts/Python/MSADNEW/ADpasswdResetNEW.py -u ${loginid}
deactivate
