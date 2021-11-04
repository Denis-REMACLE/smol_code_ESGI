import os
import sys
import platform
import re
import subprocess
import ipaddr

if len(sys.argv) == 2 and sys.argv[1] == "-h":
    print("Ce programme va récupérer les info réseaux d'une machine Linux ou Windows et les sauvergarder sur un fichier puis ressorit les adresses IP présentes")
    exit()

OS = platform.system()
print("\n My os in my system is ",OS)

if OS == "Linux":

    # Check for root privileges
    if os.geteuid()!=0:
        print("You need sudo for that")
        exit()

    os.system("ip a > network.txt")
    path = subprocess.check_output("pwd").decode().strip()
    path = path  + "/network.txt"

    if os.path.isfile(path) == False:
        print("\nFile wasn't created")
        exit()
    
    list = os.listdir(".")
    print("\nDirectory content\n")
    for i in range (len(list)):
        print(list[i])
    
    choices = {}
    number = 0
    print("\nHere are available IP address \n")
    os.system("grep 'inet ' network.txt | awk '{print $2}' > ip_available")
    with open("ip_available", "r") as ips:
        for ip in ips:
            usable_ip = ip.strip("\n")
            print("[%i] : \t%s" %(number, usable_ip))
            choices[str(number)] = usable_ip
            number += 1
    
    os.remove("network.txt")
    os.remove("ip_available")
    userChoice = str(input("\nPlease choose the ip you want to target : "))

    while userChoice not in choices:
        print("\nThis is not quite right !")
        userChoice = str(input("\nPlease choose the ip you want to target : "))

    target = ipaddr.IPv4Network(choices[userChoice])

    # Get all hosts on that network
    all_hosts = target.iterhosts()
    connected_hosts = []
    print()

    for host in all_hosts:
        output = subprocess.Popen(['ping', '-w', '1', '-W', '1', str(host)], stdout=subprocess.PIPE).communicate()[0]
        if "icmp_seq=1" in output.decode('utf-8'):
            connected_hosts.append(host)
            print(str(host), "is Online")
    print()
    for i in range(len(connected_hosts)):
        nom_fichier = str(connected_hosts[i]).replace(".", "-")+"_scan"
        print("scanning "+str(connected_hosts[i]))
        os.system("nmap -sT "+str(connected_hosts[i])+" | grep 'open' > "+ nom_fichier)
        print("Complete")
        os.system("chmod 666 "+nom_fichier)





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
    
    choices = {}
    number = 0
    print("\n Voici vos adresses IP \n")
    os.system("findstr IPv4 ipconfig.txt > ipv4use.txt")
    with open("ipv4use.txt", "r") as ips:
        for ip in ips:
            usable_ip = ip.split(':')[1]
            usable_ip = usable_ip.strip("\n")
            usable_ip = usable_ip.strip(" ")
            print("[%i] : \t%s" %(number, usable_ip))
            choices[str(number)] = usable_ip
            number+=1

    os.remove("ipv4use.txt")
    userChoice = str(input("\nPlease choose the ip you want to target : "))

    while userChoice not in choices:
        print("\nThis is not quite right !")
        userChoice = str(input("\nPlease choose the ip you want to target : "))

    target = ipaddr.IPv4Network(choices[userChoice])

    # Get all hosts on that network
    all_hosts = target.iterhosts()
    connected_hosts = []

    for host in all_hosts:
        output = subprocess.Popen(['ping', '/w', '1', '/W', '1', str(host)], stdout=subprocess.PIPE).communicate()[0]
        if "icmp_seq=1" in output.decode('utf-8'):
            connected_hosts.append(host)
            print(str(host), "is Online")

else:
    print("Pas d'OS supporté")
