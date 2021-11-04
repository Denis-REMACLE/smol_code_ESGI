import os
import sys
import platform
import re
import subprocess
import ipaddress

if len(sys.argv) == 2 and sys.argv[1] == "-h":
    print("Ce programme va récupérer les info réseaux d'une machine Linux ou Windows et les sauvergarder sur un fichier puis ressorit les adresses IP présentes")
    exit()

OS = platform.system()
print("\n My os in my system is ",OS)

if OS == "Linux":

    os.system("ip a > network.txt")
    path = subprocess.check_output("pwd").decode().strip()
    path = path  + "/network.txt"

    if os.path.isfile(path) == False:
        print("\n Le fichier .txt n'a été créé")
        exit()
    
    list = os.listdir(".")
    print("\n Contenu du dossier\n")
    for i in range (len(list)):
        print(list[i])
    
    choices = {}
    number = 0
    print("\n Voici vos adresses IP \n")
    os.system("grep inet network.txt | awk '{print $2}' > ip_available")
    with open("ip_available", "r") as ips:
        for ip in ips:
            print("[%i] : \t%s" %(number, ip.strip("\n")))
            choices[str(number)] = ip.strip("\n")
            number += 1
    
    os.remove("ip_available")
    userChoice = str(input("\nPlease choose the ip you want to target : "))

    while userChoice not in choices:
        print("\nThis is not quite right !")
        userChoice = str(input("\nPlease choose the AP you want to target : "))

    target = ipaddress.IPv4Network(choices[userChoice])
    print(target.hostmask)

elif OS == "Windows":

    os.system("ipconfig > ipconfig.txt")
    path = os.getcwd() + "\ipconfig.txt"

    if os.path.isfile(path) == False:
        print("\n le fichier .txt n'a été créé \n")
        exit()

    list = os.listdir(".")
    print("\n Contenu du dossier \n")
    for i in range (len(list)):
        print(list[i])

    print("\n Voici vos adresses IP \n")
    os.system("findstr IPv4 ipconfig.txt")

else:
    print("Pas d'OS supporté")
