#!/bin/bash
#
# Author : Denis REMACLE
# 

# set -e
# set -x
clear

function install_utils
{
        apt update && apt upgrade -y
        apt install vim sudo rsync git net-tools mlocate htop screen figlet -y
}

function install_cheat
{
	# Téléchargement de cheat
	wget https://github.com/cheat/cheat/releases/download/4.2.3/cheat-linux-amd64.gz

	# Décompresser le programme
	gunzip cheat-linux-amd64.gz

	# Autoriser l'exécution à tout les utilisateurs
	chmod a+x cheat-linux-amd64

	# Déplacer le programme vers /usr/local/bin/
	mv -v cheat-linux-amd64 /usr/local/bin/cheat
}

function uninstall_cheat
{
	rm -f /usr/local/bin/cheat
}

function create_dirs
{
	# Créer les dossiers pour la conf
	mkdir -vp /opt/COMMUN/cheat/cheatsheets/community
	mkdir -v /opt/COMMUN/cheat/cheatsheets/personal
}

function configure_cheat
{
	# Générer la conf pour le script dans le bon fichier
	cheat --init > /opt/COMMUN/cheat/conf.yml

	# Changer le path de la conf générée
	sed -i 's;/root/.config/; /opt/COMMUN/;' /opt/COMMUN/cheat/conf.yml
}

function install_cheatsheets
{
	# télécharger les cheatsheets
	git clone https://github.com/cheat/cheatsheets.git

	# Les déplacer dans le dossier créé précédement
	mv -v cheatsheets/* /opt/COMMUN/cheat/cheatsheets/community
}

function config_dir_making
{
	# Créer les dossier .config chez root et /etc/skel
	mkdir -v /root/.config/
	mkdir -v /etc/skel/.config/
	make_root_bashrc
	make_skel_bashrc
}

function make_root_bashrc
{
	echo "umask 007" >> /root/.bashrc
	cat >> /root/.bashrc << EOF
	export PS1="\[\033[38;5;1m\]\n[\t] \u@\h \w\n\\$ :\[$(tput sgr0)\] \[$(tput sgr0)\]"
	alias ll='ls -rtl'
	alias la='ls -lsa'
	alias rm='rm -Iv --preserve-root'
	alias chown="chown -v --preserve-root"
	alias chmod="chmod -v --preserve-root"
	alias chgrp="chgrp -v --preserve-root"
	alias su="su - "
	alias hs='history|grep -i '
EOF
}

function make_skel_bashrc
{
	echo "umask 007" >> /etc/skel/.bashrc
	cat >> /etc/skel/.bashrc << EOF
	export PS1="\[\033[38;5;14m\]\n[\t]\u@\h \w\n\\$ :\[$(tput sgr0)\] \[$(tput sgr0)\]"
	alias ll='ls -rtl'
	alias la='ls -lsa'
	alias rm='rm -Iv --preserve-root'
	alias chown="chown -v --preserve-root"
	alias chmod="chmod -v --preserve-root"
	alias chgrp="chgrp -v --preserve-root"
	alias su="su - "
	alias hs='history|grep -i '
EOF
}

function make_user_bashrc
{
	echo "umask 007" >> /home/$1/.bashrc
	cat >> /home/$1/.bashrc << EOF
	export PS1="\[\033[38;5;14m\]\n[\t]\u@\h \w\n\\$ :\[$(tput sgr0)\] \[$(tput sgr0)\]"
	alias ll='ls -rtl'
	alias la='ls -lsa'
	alias rm='rm -Iv --preserve-root'
	alias chown="chown -v --preserve-root"
	alias chmod="chmod -v --preserve-root"
	alias chgrp="chgrp -v --preserve-root"
	alias su="su - "
	alias hs='history|grep -i '
EOF
}

function group_create
{
	# Créer un groupe commun pour les droits sur les cheatsheets
	groupadd -g 10000 commun
	chgrp -Rv commun /opt/COMMUN
	chmod -Rv 2770 /opt/COMMUN/cheat/cheatsheets/personal
}

function config_linking
{
	# Créer les liens symboliques pour les utilisateurs
	ln -vs /opt/COMMUN/cheat /root/.config/cheat
	ln -vs /opt/COMMUN/cheat /etc/skel/.config/cheat

	# Récupérer une liste des utilisateur "legité
	users=($(grep '/bin/bash' /etc/passwd | awk -F : '{print $1}'))

	# Dans une boucle créer le dossier .config faire le lien symbolique et un ajouts aux groupes
	# Pour chaque utilisateurs sauf root
	for user in "${users[@]}"; do
		if [ $user != "root" ];
		then
			usermod -a -G commun $user
			usermod -a -G sudo $user
			mkdir /home/$user/.config
			ln -vs /opt/COMMUN/cheat /home/$user/.config/cheat
			chown -R $user /home/$user/.config
			make_user_bashrc $user
		fi
	done
}

function password_generator
{
	password=$(< /dev/urandom tr -dc a-zA-Z0-9 | head -c10)
	echo $1":"$password >> passwords
}

function create_users
{
	useradd -G sudo,commun -s /bin/bash --create-home $1
	password_generator $1
	yes $password | passwd $1

}

function create_user_UID_GID_with_sudo
{
	useradd -G sudo,commun -s /bin/bash --create-home -g $2 -u $3 $1
	passwd
}

function create_user_UID_GID
{
	useradd -G commun -s /bin/bash --create-home -g $2 -u $3 $1
	passwd
}

function banner_install
{
	echo "" > /etc/motd
	touch /etc/profile.d/mymotd.sh
	echo "hostname | figlet" >> /etc/profile.d/mymotd.sh
	echo "cat /etc/motd_for_sacking" >> /etc/profile.d/mymotd.sh
	cat >> /etc/motd_for_sacking << EOF

Hello dear user,

You may use this server responsibly and be mindful of the commands type.
Or there will be trouble !

Cheerfully,
Your system administrator

EOF
	echo "who" >> /etc/profile.d/mymotd.sh
	chmod 766 /etc/motd_for_sacking
	chmod +x /etc/profile.d/mymotd.sh
}

echo "Installing utils"
echo "__________________________"
install_utils
sleep 5
clear

echo "Installing cheat"
echo "__________________________"
install_cheat
sleep 5
clear

echo "Creating directories"
echo "__________________________"
create_dirs
sleep 5
clear

echo "Configuring cheat"
echo "__________________________"
configure_cheat
sleep 5
clear

echo "Installing cheatsheets"
echo "__________________________"
install_cheatsheets
sleep 5
clear

echo "Making .config directories"
echo "__________________________"
config_dir_making
sleep 5
clear

echo "Creating group commun"
echo "__________________________"
group_create
sleep 5
clear

echo "Linking configurations"
echo "__________________________"
config_linking
sleep 5
clear

echo "Installing motd"
echo "__________________________"
banner_install
sleep 5
clear

if [ $# -gt 0 ] && ( [ $1 == "-i" ] || [ $1 == "--interactive" ]; then
	echo "Creating custom user"
	echo "__________________________"
	echo "Please input the number of users you want to create"
	input number
	for i in {0..$number..1}
		echo "Please name the user"
		input name
		echo "Please give the uid"
		input uid
		echo "Please give the gid"
		input gid
		echo "Do you want the user to be able to use sudo : (y)es / (n)o"
		input sudo
		
		while [ $sudo  != "yes"] ||  [ $sudo != "y" ] ||  [ $sudo != "n" ] ||  [ $sudo != "no" ]
		do
			echo "Do you want the user to be able to use sudo : (y)es / (n)o"
			input sudo
		done

		if [ $sudo == "yes" ] ||  [ $sudo == "y" ]; then
			create_user_UID_GID_with_sudo $uid $gid $name
		else
			create_user_UID_GID $uid $gid $name
		
		sleep 5
		clear
else if  [ $# -gt 0 ]; then
	echo "Creating users"
	echo "__________________________"
	for user in "$@"; do
		create_users $user
	done
	sleep 5
	clear
fi