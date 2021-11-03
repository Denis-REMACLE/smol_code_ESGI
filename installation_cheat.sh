#!/etc/bin sh
clear

# Téléchargement de cheat
wget https://github.com/cheat/cheat/releases/download/4.2.3/cheat-linux-amd64.gz

# Décompresser le programme
gunzip cheat-linux-amd64.gz

# Autoriser l'exécution à tout les utilisateurs
chmod a+x cheat-linux-amd64

# Déplacer le programme vers /usr/local/bin/
mv -v cheat-linux-amd64 /usr/local/bin/cheat

# Installer git
apt install git -y

# Créer les dossiers pour la conf
mkdir -p /opt/COMMUN/cheat/cheatsheets/community
mkdir /opt/COMMUN/cheat/cheatsheets/personal

# Générer la conf pour le script dans le bon fichier
cheat --init > /opt/COMMUN/cheat/conf.yml

# Changer le path de la conf générée
sed -i 's;/root/.config/; /opt/COMMUN/;' /opt/COMMUN/cheat/conf.yml

# télécharger les cheatsheets
git clone https://github.com/cheat/cheatsheets.git

# Les déplacer dans le dossier créé précédement
mv -v cheatsheets/* /opt/COMMUN/cheat/cheatsheets/community

# Créer les dossier .config chez root et /etc/skel
mkdir /root/.config/
mkdir /etc/skel/.config/

# Créer un groupe commun pour les droits sur les cheatsheets
groupadd commun
chgrp commun /opt/COMMUN
chgrp -Rv commun /opt/COMMUN
chmod 2770 /opt/COMMUN/

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
		usermod -aG commun $1
		usermod -aG sudo $1
		mkdir /home/$i/.config
		ln -s /opt/COMMUN/cheat /home/$i/.config/cheat

	fi
done
