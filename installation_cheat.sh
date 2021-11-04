#!/bin/bash
set -e
set -x
clear

function install_utils
{
        apt update && apt upgrade -y
        apt install vim sudo rsync git net-tools mlocate top screen -y
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

function install_utils
{
	# Installer git
	apt install git -y
}

function create_dirs
{
	# Créer les dossiers pour la conf
	mkdir -p /opt/COMMUN/cheat/cheatsheets/community
	mkdir /opt/COMMUN/cheat/cheatsheets/personal
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
	mkdir /root/.config/
	mkdir /etc/skel/.config/
	make_root_bashrc
	make_skel_bashrc
}

function make_root_bashrc
{
	echo "umask 007" >> /root/.bashrc
	cat >> /root/.bashrc << EOF
	export PS1='\e[0;35m\n[\t] \u@\h : \w\n\$ : \e[m'
	alias ll='ls -rtl'
	alias la='ls -lsa'
	alias rm='rm -Iv --preserve-root'
	alias chown="chown -v --preserve-root"
	alias chmod="chmod -v --preserve-root"
	alias chgrp="chgrp -v --preserve-root"
EOF
}

function make_skel_bashrc
{
	echo "umask 007" >> /etc/skel/.bashrc
	cat >> /etc/skel/.bashrc << EOF
	export PS1='\e[0;35m\n[\t] \u@\h : \w\n\$ : \e[m'
	alias ll='ls -rtl'
	alias la='ls -lsa'
	alias rm='rm -Iv --preserve-root'
	alias chown="chown -v --preserve-root"
	alias chmod="chmod -v --preserve-root"
	alias chgrp="chgrp -v --preserve-root"
EOF
}

function make_user_bashrc
{
	echo "umask 007" >> /home/$1/.bashrc
	cat >> /home/$1/.bashrc << EOF
	export PS1='\e[0;35m\n[\t] \u@\h : \w\n\$ : \e[m'
	alias ll='ls -rtl'
	alias la='ls -lsa'
	alias rm='rm -Iv --preserve-root'
	alias chown="chown -v --preserve-root"
	alias chmod="chmod -v --preserve-root"
	alias chgrp="chgrp -v --preserve-root"
EOF
}

function group_create
{
	# Créer un groupe commun pour les droits sur les cheatsheets
	groupadd commun
	chgrp -Rv commun /opt/COMMUN
	chmod -Rv 2770 /opt/COMMUN/
}

function config_linking
{
	# Créer les liens symboliques pour les utilisateurs
	ln -s /opt/COMMUN/cheat /root/.config/cheat
	ln -s /opt/COMMUN/cheat /etc/skel/.config/cheat

	# Récupérer une liste des utilisateur "legité
	users=($(grep '/bin/bash' /etc/passwd | awk -F : '{print $1}'))

	# Dans une boucle créer le dossier .config faire le lien symbolique et un ajouts aux groupes
	# Pour chaque utilisateurs sauf root
	for user in "${users[@]}"; do
		if [ $i != "root" ];
		then
			usermod -a -G commun $user
			usermod -a -G sudo $user
			mkdir /home/$user/.config
			ln -s /opt/COMMUN/cheat /home/$user/.config/cheat
			chown -R $i /home/$user/.config

		fi
	done

	umask 007 /opt/COMMUN/cheat/cheatsheets
}

function create_users
{
	for user in "$@"; do
		useradd -G sudo, commun -s /bin/bash --create-home $user
		make_user_bashrc $user
	done
}

function create_user_UID_GID
{
	useradd -G sudo, commun -s /bin/bash --create-home -g $2 -u $3 $1
	echo -e $4"\n"$4 | passwd $1
}

install_utils
install_cheat
create_dirs
configure_cheat
install_cheatsheets
config_dir_making
group_create
config_linking
create_users denis
create_user_UID_GID esgi 1000 1000 Pa55w.rd
