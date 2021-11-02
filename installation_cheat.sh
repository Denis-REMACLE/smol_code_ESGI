#!/etc/bin sh
clear
wget https://github.com/cheat/cheat/releases/download/4.2.3/cheat-linux-amd64.gz

gunzip cheat-linux-amd64.gz

chmod a+x cheat-linux-amd64

mv -v cheat-linux-amd64 /usr/local/bin/cheat

apt install git -y

mkdir -p /opt/COMMUN/cheat/cheatsheets/community
mkdir /opt/COMMUN/cheat/cheatsheets/personal

cheat --init > /opt/COMMUN/cheat/conf.yml

sed -i 's;/root/.config/; /opt/COMMUN/;' /opt/COMMUN/cheat/conf.yml
git clone https://github.com/cheat/cheatsheets.git

mv -v cheatsheets/* /opt/COMMUN/cheat/cheatsheets/community

mkdir /root/.config/
mkdir /etc/skel/.config/

groupadd commun
chgrp commun /opt/COMMUN
chgrp -Rv commun /opt/COMMUN
chmod 2770 /opt/COMMUN/

ln -s /opt/COMMUN/cheat /root/.config/cheat
ln -s /opt/COMMUN/cheat /etc/skel/.config/cheat

users=($(grep '/bin/bash' /etc/passwd | awk -F : '{print $1}'))
for i in "${users[@]}"; do
	if [ $i != "root" ];
	then
		usermod -aG commun $1
		usermod -aG sudo $1
		mkdir /home/$i/.config
		ln -s /opt/COMMUN/cheat /home/$i/.config/cheat

	fi
done
