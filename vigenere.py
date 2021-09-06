#!/usr/bin/env python3
import argparse

def cryptor(texte, clef):

    code = ""
    while len(texte) > len(clef):
        clef+=clef

    for i in range(len(texte)):
    
        if texte[i].isupper():
            lettre = ord(texte[i])-65
        else:
            lettre = ord(texte[i])-97
        crypto = ord(clef[i])-65
        chiffre = lettre + crypto
        
        if texte[i].isupper():
            code+=chr(chiffre%26+65)
        else:
            code+=chr(chiffre%26+97)

    return code

def decryptor(code, clef):
    
    texte = ""
    while len(code) > len(clef):
        clef+=clef

    for i in range(len(code)):

        if code[i].isupper():
            lettre = ord(code[i])-65
        else:
            lettre = ord(code[i])-97
        crypto = ord(clef[i])-65
        dechiffre = lettre - crypto

        if code[i].isupper():
            texte+=chr(dechiffre%26+65)
        else:
            texte+=chr(dechiffre%26+97)

    return texte

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--texte", type=str)
    parser.add_argument("--code", type=str)
    parser.add_argument("--key", type=str)

    args = parser.parse_args()

    if args:
        if args.texte and args.code:
            print("This ain't good")
        elif args.texte:
            code = cryptor(args.texte, args.key)
            print(code)
        elif args.code:
            texte = decryptor(args.code, args.key)
            print(texte)
        else:
            print("This ain't good")
    else:
        end = False

        while end == False:
            print("What would you like to do ? (E)ncrypt, (D)ecrypt or E(x)it")
            reponse = input()
            if reponse == "x" or reponse == "X":
                end = True
                continue
            elif reponse == "e" or reponse == "E":
                print("You chose to encrypt data")
                print("Please provide the data")
                texte = input()
                print("Please Provide the key")
                clef = input()
                code = cryptor(texte, clef)
                print("Encryped data looks like : " + code)
            elif reponse == "d" or reponse == "D":
                print("You chose to decrypt data")
                print("Please provide the data")
                code = input()
                print("Please provide the key")
                clef = input()
                texte = decryptor(code, clef)
                print("Decrypted data looks like : " + texte)
            else:
                print("That ain't good")
                continue
