#!/bin/bash
set -e
set -x
clear

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

function install_git
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
}

function group_create
{
	# Créer un groupe commun pour les droits sur les cheatsheets
	groupadd commun
	chgrp -Rv commun /opt/COMMUN
	chmod -Rv 2770 /opt/COMMUN/
	umask 007 /opt/COMMUN/cheat/cheatsheets
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
	for i in "${users[@]}"; do
		if [ $i != "root" ];
		then
			usermod -a -G commun $i
			usermod -a -G sudo $i
			mkdir /home/$i/.config
			ln -s /opt/COMMUN/cheat /home/$i/.config/cheat
			chown -R $i /home/$i/.config

		fi
	done
}

install_cheat
install_git
create_dirs
configure_cheat
install_cheatsheets
config_dir_making
group_create
config_linking

