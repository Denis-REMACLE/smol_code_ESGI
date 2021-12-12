import winreg as reg
import subprocess
import ctypes
import argparse
import os

def ProgramOnStartup(name_program):
    
    # in python __file__ is the instant of
    # file path where it was executed
    # so if it was executed from desktop,
    # then __file__ will be
    # c:\users\current_user\desktop
    #pth = os.path.dirname(os.path.realpath(__file__))
    
    # name of the python file with extension
    #s_name=name_program
    address=name_program
    
    # joins the file name to end of path address
    #address=pth.join(s_name)
    
    # key we want to change is HKEY_CURRENT_USER
    # key value is Software\Microsoft\Windows\CurrentVersion\Run
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
    
    # open the key to make changes to
    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
    
    # modify the opened key
    reg.SetValueEx(open,"any_name",0,reg.REG_SZ,address)
    
    # now close the opened key
    reg.CloseKey(open)

def UnProgramOnStartup(name_program):
    
    # in python __file__ is the instant of
    # file path where it was executed
    # so if it was executed from desktop,
    # then __file__ will be
    # c:\users\current_user\desktop
    #pth = os.path.dirname(os.path.realpath(__file__))
    
    # name of the python file with extension
    #s_name=name_program
    address=name_program
    
    # joins the file name to end of path address
    #address=pth.join(s_name)
    
    # key we want to change is HKEY_CURRENT_USER
    # key value is Software\Microsoft\Windows\CurrentVersion\Run
    key = reg.HKEY_CURRENT_USER
    key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
    
    # open the key to make changes to
    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
    
    # modify the opened key
    reg.DeleteKey(open,"any_name")
    
    # now close the opened key
    reg.CloseKey(open)

def ReadWirelessNetworks():
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
    result = result.decode('gbk')
    lst = result.split('\r\n')
    lst = lst[4:]
    networks = "Available wifi networks are : \n"

    for index in range(len(lst)):
        if index % 5 == 0:
            networks += (lst[index] + "\n")
    ctypes.windll.user32.MessageBoxA(0, b"Networks available", bin(networks), 0)

def ReadOnlyUSB():
    key = reg.HKEY_LOCAL_MACHINE
    key_value = "\SYSTEM\CurrentControlSet\Control\StorageDevicePolicies"
    
    # open the key to make changes to
    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
    
    # modify the opened key
    reg.SetValueEx(open,"WriteProtect",0,reg.REG_SZ,1)

def UnReadOnlyUSB():
    key = reg.HKEY_LOCAL_MACHINE
    key_value = "\SYSTEM\CurrentControlSet\Control\StorageDevicePolicies"
    
    # open the key to make changes to
    open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
    
    # modify the opened key
    reg.SetValueEx(open,"WriteProtect",0,reg.REG_SZ,0)


if __name__=="__main__":

    parser.add_argument("--do", default=False, action="store_true")
    parser.add_argument("--undo", default=False, action="store_true")
    args = parser.parse_args()

    name_program = "C:\Windows\WinSxS\wow64_microsoft-windows-calc_31bf3856ad364e35_10.0.19041.1_none_6a03b910ee7a4073\calc.exe"

    if args.do:
        ProgramOnStartup(name_program)
        ReadWirelessNetworks()
        ReadOnlyUSB()
    
    if args.undo:
        UnProgramOnStartup(name_program)
        UnReadOnlyUSB()