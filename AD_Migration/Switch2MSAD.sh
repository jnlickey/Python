#!/bin/bash
#####################################################################################################
#
# This script was created to join Ubuntu servers to Microsoft AD.
# 
# Created by: J.Lickey
# 2022/01/13
#
#####################################################################################################

# Verifies that the hostname on the server is setup properly
function Set_Hostname() {
	CHK_HOST=$(hostname -f)
	if [[ ${CHK_HOST} = '' ]];then
        	IP=$(ip a | grep -oP "(?<=inet )\S+" | tail -n 1 | cut -d"/" -f1)
        	sed -i "3 i ${IP} ${HOSTNAME}.${new_DN_Lower} ${HOSTNAME}\n" /etc/hosts
	fi
}

# Sets up time synchronization between MS AD server and client, so kerberos works
function Sync_Time() {
        CHK_NTP=$(egrep "\#NTP|\#Fall" /etc/systemd/timesyncd.conf)
        if [[ ${CHK_NTP} =~ \#NTP|\#Fall.+ ]];then
                sed -i "/^#NTP/ s/$/${new_DN_Lower}/ g;s/#NTP/NTP/g" /etc/systemd/timesyncd.conf
                new_servers=$(echo ${new_AD_servers} | tr ',' ' ' | sed "s/ /\.${new_DN_Lower} /g;s/$/\.${new_DN_Lower}/g")
                sed -i "/^#Fall/ s/$/${new_servers}/ g;s/#Fall/Fall/g;s/ntp.ubuntu.com//g" /etc/systemd/timesyncd.conf
                timedatectl set-ntp true
                timedatectl set-timezone America/Los_Angeles
                systemctl restart systemd-timesyncd.service
                timedatectl --adjust-system-clock
        fi
        # Check if it worked
        txt="Time Sync Status"
        #CHECK=$(timedatectl status | grep -oP "(?<=NTP service\:\s)\S+")
        CHECK=$(cat /etc/systemd/timesyncd.conf | egrep -v "\#")
        spaces=$(expr ${COLS} - ${#txt} - 10)
        if [[ ${CHECK} =~ $(echo ${new_AD_servers} | tr ',' '|') ]];then
                printf "%s%-${spaces}s [  ${BGRN}%s${NC}  ]\n" "${txt}" "" "OK"
        else
                spaces=$(expr ${COLS} - ${#txt} - 11)
                printf "%s%-${spaces}s [ ${BRED}%s${NC} ]\n" "${txt}" "" "FAILED"
        fi
}

# Builds the /etc/realmd.conf file, which is used when running the realm command to build the /etc/sssd/sssd.conf file
function Build_realmd() {
        OS=$(cat /etc/os-release | grep -oP "(?<=^NAME=)\S+" | sed 's/"//g')
        OSVERSION=$(cat /etc/os-release | grep -oP "(?<=^VERSION=)\S+" | sed 's/"//g')
        echo -ne "[users]\n" > /etc/realmd.conf
        echo -ne "default-home = /home/%U\n" >> /etc/realmd.conf
        echo -ne "default-shell = /bin/bash\n" >> /etc/realmd.conf
        echo -ne "\n" >> /etc/realmd.conf
        echo -ne "[active-directory]\n" >> /etc/realmd.conf
        echo -ne "default-client = sssd\n" >> /etc/realmd.conf
        echo -ne "os-name = ${OS}\n" >> /etc/realmd.conf
        echo -ne "os-version = ${OSVERSION}\n" >> /etc/realmd.conf
        echo -ne "\n" >> /etc/realmd.conf
        echo -ne "[service]\n" >> /etc/realmd.conf
        echo -ne "# Set this to no to disable automatic installation of packages via package-kit.\n" >> /etc/realmd.conf
        echo -ne "#automatic-install = no\n" >> /etc/realmd.conf
        echo -ne "\n" >> /etc/realmd.conf
	echo -ne "[${new_DN_Lower}]\n" >> /etc/realmd.conf
        echo -ne "fully-qualified-names = no\n" >> /etc/realmd.conf
        echo -ne "automatic-id-mapping = no\n" >> /etc/realmd.conf
        echo -ne "user-principal = yes\n" >> /etc/realmd.conf
        echo -ne "manage-system = yes\n" >> /etc/realmd.conf
        echo -ne "#computer-name = ${HOSTNAME}\n" >> /etc/realmd.conf
        echo -ne "computer-ou = CN=Computers,${new_DC_info}\n" >> /etc/realmd.conf
	modify_nsswitch
}

# Modify /etc/nsswitch.conf
function modify_nsswitch() {
	CHECK=$(grep -oP "(?<=^passwd\:)\s+\S+\s\S+" /etc/nsswitch.conf)
	if [[ ${CHECK} =~ files ]];then
		sed -i -E 's/^passwd\:[[:space:]]+files sss/passwd:\t\tcompat sss/;s/^group\:[[:space:]]+files sss/group:\t\tcompat sss/' /etc/nsswitch.conf
	fi

        txt="Modify /etc/nsswitch.conf"
	CHECK=$(grep -oP "(?<=^passwd\:)\s+\S+\s\S+" /etc/nsswitch.conf)
        space=$(expr ${COLS} - ${#txt} - 10)
        if [[ ${CHECK} =~ "compat sss" ]];then
        	printf "%s%-${space}s [  ${BGRN}%s${NC}  ]\n" "${txt}" " " "OK"
        else
                space=$(expr ${COLS} - ${#txt} - 14)
                printf "%s%-${space}s [  ${BRED}%s${NC}  ]\n" "${txt}" " " "FAILED"
        fi
}

# Modifies the /etc/sssd/sssd.conf file after the client has been joined to the MS AD domain
function Modify_SSSD() {
	if [[ ! -f /etc/sssd/sssd.conf-*.bak ]];then
		cp /etc/sssd/sssd.conf /etc/sssd/sssd.conf-${DATE}.bak
	fi
	#echo -ne "Start modifying sssd\n"
	sed -i 's/%u@%d/%u/g' /etc/sssd/sssd.conf
	sed -i 's/use_fully_qualified_names = True/use_fully_qualified_names = False/g' /etc/sssd/sssd.conf
	sed -i '/^access_provider/i ### Restrict login access to specific accounts ###' /etc/sssd/sssd.conf
	sed -i '/^access_provider/a simple_allow_groups\ \= Domain Admins\,\ Domain Users' /etc/sssd/sssd.conf 
	sed -i '/^simple_allow_groups/a chpass_provider = ad\n\n' /etc/sssd/sssd.conf

	echo -ne "### Restrict login access to specific accounts ###\n" >> /etc/sssd/sssd.conf
        echo -ne "#access_provider = ad\n" >> /etc/sssd/sssd.conf
        echo -ne "# Pick one of:\n" >> /etc/sssd/sssd.conf
        echo -ne "\n" >> /etc/sssd/sssd.conf
        echo -ne "#ad_access_filter = (group_name)\n" >> /etc/sssd/sssd.conf
        echo -ne "\n" >> /etc/sssd/sssd.conf
        echo -ne "#ad_access_filter = (|(sAMAccountName=moe)(sAMAccountName=larry)(sAMAccountName=curly))\n" >> /etc/sssd/sssd.conf
        echo -ne "#ad_access_filter = (|(manager=CN=smith,OU=Users,${new_DC_info}DC=ad,DC=cll,DC=cloud)(manager=CN=jones,OU=Users,${new_DC_info}))\n" >> /etc/sssd/sssd.conf
	echo -ne "\n" >> /etc/sssd/sssd.conf
        echo -ne "ldap_user_gecos = displayName\n" >> /etc/sssd/sssd.conf
        echo -ne "ldap_user_uid_number = uidNumber\n" >> /etc/sssd/sssd.conf
        echo -ne "ldap_user_gid_number = gidNumber\n" >> /etc/sssd/sssd.conf
        echo -ne "\n" >> /etc/sssd/sssd.conf
        echo -ne "\n" >> /etc/sssd/sssd.conf
        echo -ne "# Make account name be just username, not \"username@domain\"\n" >> /etc/sssd/sssd.conf
        echo -ne "full_name_format = %1\$s\n" >> /etc/sssd/sssd.conf
        echo -ne "\n" >> /etc/sssd/sssd.conf
        echo -ne "# Helpful for figuring out what LDAP queries are being done\n" >> /etc/sssd/sssd.conf
        echo -ne "#debug_level = 7\n" >> /etc/sssd/sssd.conf
	#echo -ne "Finished modifying sssd\n"
}

# Used for starting sssd
function Starting_SSSD() {
	systemctl start sssd.service
	txt="Starting SSSD"
	spaces=$(expr ${COLS} - ${#txt} - 10)
	chksssd=$(systemctl status sssd.service | grep -oP '(?<=Active\:\s)\w+')
	if [[ ${chksssd} = "active" ]];then
		printf "%s%-${spaces}s [  ${BGRN}%s${NC}  ]\n" "${txt}" "" "OK"
	else
		spaces=$(expr ${COLS} - ${#txt} - 11)
		printf "%s%-${spaces}s [ ${BRED}%s${NC} ]\n" "${txt}" "" "FAILED"
		exit
	fi
}

# Used for stopping sssd, when stopping the sssd cache is cleared
function Stopping_SSSD() {
	systemctl stop sssd.service 
	rm -rf /var/lib/sss/db/*
	txt="Stopping SSSD"
	spaces=$(expr ${COLS} - ${#txt} - 10)
	chksssd=$(systemctl status sssd.service | grep -oP '(?<=Active\:\s)\w+')
	if [[ ${chksssd} = "inactive" ]];then
		printf "%s%-${spaces}s [  ${BGRN}%s${NC}  ]\n" "${txt}" "" "OK"
	else
		spaces=$(expr ${COLS} - ${#txt} - 11)
		printf "%s%-${spaces}s [ ${BRED}%s${NC} ]\n" "${txt}" "" "FAILED"
		exit
	fi
}

# Builds the /etc/krb5.conf file so that kerberos works
function Modify_KRB5() {
	if [[ ! -f /etc/krb5.conf-*.bak ]];then
		cp /etc/krb5.conf /etc/krb5.conf-${DATE}.bak
	fi
	CHKDOM=$(cat /etc/krb5.conf | grep -oP "(?<=default_realm\s\=\s)${new_DN_UPPER}")
	CHKLOG=$(cat /etc/krb5.conf | grep logging)
	if [[ ${CHKDOM} = "" ]];then
	        txt="Modifed krb5"
	        spaces=$(expr ${COLS} - ${#txt} - 10)
		printf "\nModifying /etc/krb5.conf....\n"
		sed -i "/^.*${old_DN_UPPER}/s/^/#/;/^.*${old_DN_Lower}/s/^/#/;/\t\}/s/^/#/" /etc/krb5.conf
		sed -i "/^\[libdefaults\]/a \ \ \ \ \ \ \ \ default_realm = ${new_DN_UPPER}" /etc/krb5.conf
		sed -i "/^\[realms\]/a \ \ \ \ \ \ \ \ ${new_DN_UPPER} = {\n\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ kdc = ${new_DN_Lower}\n\ \ \ \ \ \ \ \ \ \ \ \ \ \ \ \ admin_server = ${new_DN_Lower}.\n\ \ \ \ \ \ \ \ }" /etc/krb5.conf
		sed -i "/^\[domain_realm\]/a \ \ \ \ \ \ \ \ .${new_DN_Lower} = ${new_DN_UPPER}\n\ \ \ \ \ \ \ \ ${new_DN_Lower} = ${new_DN_UPPER}" /etc/krb5.conf
		echo -ne "[appdefaults]\n\ pam\ \=\ {\n\ \ minimum_uid\ \=\ 1500\n}"
		if [[ ${CHKLOG} = "" ]];then
			sed -i '/^[libdefaults]/i [logging]\ndefault = FILE:/var/log/krb5libs.log\n kdc = FILE:/var/log/krb5kdc.log\n admin_server = FILE:/var/log/kadmind.log\n\n' /etc/krb5.conf
			printf "Added logging to krb5.conf\n"
		fi
		chkkrb5=$(cat /etc/krb5.conf | grep -oP "(?<=default_realm\s\=\s)${new_DN_UPPER}")
		if [[ ${chkkrb5} = "${new_DN_UPPER}" ]];then
	                printf "%s%-${spaces}s [  ${BGRN}%s${NC}  ]\n" "${txt}" "" "OK"
	        else
        	        printf "%s%-${spaces}s [  ${BRED}%s${NC}  ]\n" "${txt}" "" "FAILED"
               		exit
		fi
	fi
}

# This removes the client server from the Samba4 Univention Domain in preperation for joining MS AD domain
function LeaveDomain() {
	# CHKDOM is a local variable to LEAVEDOMAIN, checking to see if already left old domain
	CHKDOM=$(realm discover ${old_DN} | head -1)
	if [[ ${CHKDOM} = "" ]];then
		printf "${BGRN}No longer joined to ${old_DN} domain.${NC}\n"
	elif [[ ${CHKDOM} = ${new_DN_UPPER} ]];then
		printf "${BGRN}Already joined to M\$ AD domain.${NC}\n"
	else
		# $DIR is a local variable to LEAVEDOMAIN
		local DIR="${1}"
		Stopping_SSSD
		printf "\nEnter Univention ${old_admin_acct} credentials: ";read -s adminjoin;printf "\n"
		export adminjoin
		export ${old_admin_acct}
		export ${old_DN}

		# Python script below gets created and executed to leave existing old domain
		cat << EOF > ${DIR}/LeaveDomain.py
#!/usr/bin/python3 -tt
import subprocess
import pexpect

child = pexpect.spawn ('realm leave -U ${old_admin_acct} ${old_DN}', encoding='utf-8')
child.expect ('Password for ${old_admin_acct}:')
child.sendline ("${adminjoin}")
child.expect(pexpect.EOF)
print("Leaving ${old_DN} domain")
EOF

		chmod 770 ${DIR}/LeaveDomain.py
		txt=$(${DIR}/LeaveDomain.py)
		space=$(expr $COLS - ${#txt} - 10)
		#rm ${DIR}/LeaveDomain.py
		if [[ ${txt} = "Leaving ${old_DN} domain" ]];then
			printf "%s%-${space}s [  ${BGRN}%s${NC}  ]\n" "${txt}" " " "OK"
		else
			txt="realm leave -U ${old_admin_acct} ${old_DN}"
			space=$(expr ${COLS} - ${#txt} - 14)
			printf "%s%-${space}s [  ${BRED}%s${NC}  ]\n" "${txt}" " " "FAILED"
			exit
		fi
	fi
	sed -i 's/\(child.sendline \)\(.*\)/\1\("\<passwd_removed\>\"\)/' ${DIR}/LeaveDomain.py
}

# Used for joining client to MS AD domain
function JoinMSAD() {
	# Checking if already a member of AD
	CHKDOMAIN=$(realm list | head -1)
	if [[ ${CHKDOMAIN} = ${new_DN_Lower} ]];then
		printf "${BGRN}ALREADY JOINED TO M\$ Domain.${NC}\n"
		exit
	else	
		# $DIR is local variable to JoinMSAD
		local DIR="${1}"
		# Modify the /etc/krb5.conf file prior to joining MS AD
		Modify_KRB5

		# Begin joining the MS AD Domain
		printf "\nEnter MS AD ${new_admin_acct} credentials: ";read -s administrator;printf "\n"
		#export administrator
		export ${new_admin_acct}
		#export new_DN_Lower
		export ${new_DC_info}
		COMPNAME=$(hostname | tr '[a-z]' '[A-Z]')
		export COMPNAME
		OS=$(cat /etc/os-release | grep "PRETTY_NAME" | cut -d"=" -f2 | sed 's/"//g')
		export OS
		OSNAME=$(cat /etc/os-release | grep "NAME" | head -1 | cut -d"=" -f2 | sed 's/"//g')
		export OSNAME
		
		# Python script below gets created and executed to join server to MS AD domain 
		cat << EOF > ${DIR}/JoinAD.py
#!/usr/bin/python3 -tt
import subprocess
import pexpect

child = pexpect.spawn ('realm join -U ${new_admin_acct} ${new_DN_Lower} --computer-name="${COMPNAME}" --os-name="${OSNAME}" --os-version="${OS}" --computer-ou="CN=Computers,${new_DC_info}" --automatic-id-mapping=no')
child.expect ('Password for ${new_admin_acct}:')
child.sendline ("${administrator}")
child.expect(pexpect.EOF)
print('Joining ${new_DN_Lower} domain')
EOF

		chmod 770 ${DIR}/JoinAD.py
		txt=$(${DIR}/JoinAD.py)
		space=$(expr $COLS - ${#txt} - 10)
		if [[ ${txt} = "Joining ${new_DN_Lower} domain" ]];then
			printf "%s%-${space}s [  ${BGRN}%s${NC}  ]\n" "${txt}" " " "OK"

		else
			txt="realm join -U ${new_admin_acct} ${new_DN_Lower} --computer-name=\"${COMPNAME}\" --os-name=\"${OSNAME}\" --os-version=\"${OS}\" --computer-ou=\"CN=Computers,${new_DC_info}\" --automatic-id-mapping=\"no\""
			space=$(expr ${COLS} - ${#txt} - 14)
			printf "%s%-${space}s [  ${BRED}%s${NC}  ]\n" "${txt}" " " "FAILED"
			exit
		fi
	fi
	sed -i 's/\(child.sendline \)\(.*\)/\1\("\<passwd_removed\>\"\)/' ${DIR}/JoinAD.py
}

# Verifies and Installs needed packages for joining Ubuntu to MS AD
function CheckInstalledPkgs() {
	PKGS="python3,realmd,sssd,sssd-tools,sssd,libnss-sss,libpam-sss,adcli,samba-common-bin,krb5-user"
	printf "Checking for needed packages.....\n"
	for p in $(echo ${PKGS} | tr ',' ' ');do
		pkg=$(dpkg -l | grep $p | head -1 | awk '{print $1" "$2}')
		if [[ ${pkg} =~ python ]] || [[ ${pkg} =~ ^ii.* ]];then
			pkg=$(dpkg -l | grep -oP $p | head -1)
		fi
		if [[ ${pkg} = "" ]] || [[ ${pkg} =~ ^rc.* ]];then
			txt="${p} Installed"
			space=$(expr ${COLS} - ${#txt} - 14)
			printf "%s%-${space}s [  ${BRED}%s${NC}  ]\n" "${txt}" " " "FAILED"
		else
			txt="${pkg} Installed"
			space=$(expr ${COLS} - ${#txt} - 10)
			printf "%s%-${space}s [  ${BGRN}%s${NC}  ]\n" "${txt}" " " "OK"
		fi
	done | tee /tmp/check_installed.txt
	
	FAIL=$(grep -i fail /tmp/check_installed.txt)
	if [[ ! $FAIL = "" ]];then
		printf "\n"
		# Stop script not ready for MS AD 
		exit
	fi
}

# Adds the correct AD search function in /etc/resolv.conf
function add_search() {
        CHECK=$(cat /etc/resolv.conf | grep -oP "(?<=search )\S+\s\S+")
	if [[ ! ${CHECK} =~ ad ]];then
		sed -i "/search / s/$/ ${new_DN_Lower}/" /etc/resolv.conf
	fi
}

# Verifies and sets up DNS so that the client can join MS AD domain correctly
function CheckDNS() {
	printf "Checking DNS Setup.....\n"
	DNS=$(egrep "$(echo ${DNS_ip} | tr ',' '|')" /etc/resolv.conf)
	if [[ $DNS = "" ]];then
		printf "Installing/Setting up resolvconf..."
	    	apt install resolvconf -y 1>/dev/null 2>/dev/null
	    	/bin/systemctl start resolvconf.service
	    	/bin/systemctl enable resolvconf.service
	    	if [[ ! $(dpkg -l | grep resolvconf) = "" ]];then
	    		if [[ ! $(cat /etc/resolvconf/resolv.conf.d/head) =~ $(echo ${DNS_ip} | tr ',' '|') ]];then
				printf "$(echo ${DNS_ip} | tr ',' '\n')\n" >> /etc/resolvconf/resolv.conf.d/head
				sed -i '/^[0-9]/ s/./nameserver &/' /etc/resolvconf/resolv.conf.d/head
	    		fi
	    	fi
	    	/bin/systemctl restart resolvconf.service
	    	/usr/sbin/resolvconf -u
	    	if [[ $(cat /etc/resolv.conf | grep -v "\#") =~ $(echo ${DNS_ip} | tr ',' '|') ]];then
	    		txt="DNS Setup"
	   		space=$(expr ${COLS} - ${#txt} - 10)
	    		printf "%s%-${space}s [  ${BGRN}%s${NC}  ]\n" "${txt}" " " "OK"
	    	else
	    		txt="DNS Setup"
	    		space=$(expr ${COLS} - ${#txt} - 15)
	    		printf "%s%-${space}s [  ${BRED}%s${NC}  ]\n" "${txt}" " " "FAILED"
	    	fi
	    else
	    	txt="DNS Setup"
	    	space=$(expr ${COLS} - ${#txt} - 10)
	    	printf "%s%-${space}s [  ${BGRN}%s${NC}  ]\n" "${txt}" " " "OK"
	    fi
	add_search	
}

# Sets up pam configuation so that home directories are created when a user logs in after the client is joined to MS AD domain
function Modify_Pam() {
        CHECK=$(grep "skel\=" /etc/pam.d/common-session)
        if [[ ${CHECK} = '' ]];then
                sed -i '/\# end of pam-auth.*/i session required        pam_mkhomedir.so skel=/etc/skel/ umask=0022' /etc/pam.d/common-session
        fi
        txt="Modify /etc/pam.d/common-session"
        CHECK=$(grep -oP "(?<=pam_mkhomedir.so )\S+\s\S+" /etc/pam.d/common-session)
        space=$(expr ${COLS} - ${#txt} - 10)
        if [[ ${CHECK} =~ 0022 ]];then
                printf "%s%-${space}s [  ${BGRN}%s${NC}  ]\n" "${txt}" " " "OK"
        else
                txt="/etc/pam.d/common-session missing skel=/etc/skel/ umask=0022"
                space=$(expr ${COLS} - ${#txt} - 14)
                printf "%s%-${space}s [  ${BRED}%s${NC}  ]\n" "${txt}" " " "FAILED"
        fi
}

# =========================  MAIN BASH SCRIPT  =========================

# BASH Colors
BRED='\033[91;1m'
GRN='\033[92;3m'
BGRN='\033[92;1m'
BYEL='\033[93;1m'
BCYN='\033[96;1m'
NC='\033[0m'

# Grab today's date for creating backups
DATE=$(date +"%Y%m%d")

# Get Terminal size
COLS=$(tput cols)
ROWS=$(tput lines)

# Inform users what the script is for when executing. Stop gap
printf "*** ${BYEL}WARNING${NC} *** This script is for changing from Univention AD to Microsoft AD.\n"
printf "${GRN}Do you want to continue (Y|N):${NC} ";read ans

if [[ $ans =~ [Y|y][E|e][S|s]|[Y|y] ]];then 
	# Check to see if user is root
	if [[ ${USER} = "root" ]];then
		# Check to see if scripts directory exists
		if [[ ! -d /usr/local/scripts/MSADsetup ]];then
			mkdir -p /usr/local/scripts/MSADsetup 
			MSADDIR='/usr/local/scripts/MSADsetup'
		else
			MSADDIR="/usr/local/scripts/MSADsetup"
		fi
		
		# Gather DNS IP information
		printf "Enter DNS Server IP information [172.17.0.53,172.27.0.53]";read DNS_ip
		if [[ ${DNS_ip} = '' ]];then
			DNS_ip="172.17.0.53,172.27.0.53"
		fi

		# Gather Old Domain information
		printf "Enter ${BCYN}OLD${NC} domain name: ";read old_DN
		printf "Enter ${BCYN}OLD${NC} domain admin account [admin_join]: ";read old_admin_acct
		if [[ ${old_admin_acct} = '' ]];then
			old_admin_acct="admin_join"
		fi

		# Gather NEW Domain information
		printf "Enter ${BYEL}NEW${NC} domain name: ";read new_DN
		printf "Enter ${BYEL}NEW${NC} domain server short names [sj-wad-prod-01,rtp-wad-prod-01]: ";read new_AD_servers
		if [[ ${new_AD_servers} = '' ]];then
			new_AD_servers="sj-wad-prod-01,rtp-wad-prod-01"
		fi
		printf "Enter ${BYEL}NEW${NC} domain admin account, MS AD default is Administrator [Administrator]: ";read new_admin_acct
		if [[ ${new_admin_acct} = '' ]];then
			new_admin_acct="Administrator"
		fi

		# Sets Domain names to Upper Case
		old_DN_UPPER=$(echo ${old_DN} | tr '[a-z]' '[A-Z]')
		new_DN_UPPER=$(echo ${new_DN} | tr '[a-z]' '[A-Z]')

		# Sets Domain names to Lower Case
		old_DN_Lower=$(echo ${old_DN} | tr '[A-Z]' '[a-z]')
		new_DN_Lower=$(echo ${new_DN} | tr '[A-Z]' '[a-z]')
		
		# Create new DC Information, in the form of: DC=ad,DC=example,DC=com
		new_DC_info=$(echo "${new_DN_Lower}" | tr '.' ' ' | sed 's/^/DC\=/;s/\ /,DC=/g')
		old_DC_info=$(echo "${old_DN_Lower}" | tr '.' ' ' | sed 's/^/DC\=/;s/\ /,DC=/g')

		# Call above functions
		CheckInstalledPkgs
		CheckDNS ${DNS_ip}
		LeaveDomain ${MSADDIR}
		Set_Hostname
		Build_realmd
		Modify_KRB5
		Sync_Time
		Modify_Pam
		JoinMSAD ${MSADDIR}
		Modify_SSSD ${DATE}
		Stopping_SSSD
		Starting_SSSD
		
	else
		printf "You are not ${BGRN}root${NC}.\nThis script should be ran as root user.\n"
		exit
	fi
fi
exit 0
