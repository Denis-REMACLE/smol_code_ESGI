#!/usr/bin/env python3
import argparse

def cryptor(texte, clef):
    # Encript text using vigenere cypher
    code = ""
    while len(texte) > len(clef):
         # Need to make sure encryption key is long enough
         clef+=clef

    for i in range(len(texte)):
        
        # Making the script case sensitive
        if texte[i].isupper():
            code+=chr(((ord(texte[i])-65)+(ord(clef[i])-97))%26+65)
        else:
            code+=chr(((ord(texte[i])-97)+(ord(clef[i])-97))%26+97)

    return code

def decryptor(code, clef):
    # Decrypt text using vigenere cypher
    texte = ""
    while len(code) > len(clef):
        # Need to make sure encryption key is long enough
        clef+=clef

    for i in range(len(code)):

        # Making the script case sensitive
        if texte[i].isupper():
            texte+=chr(((ord(code[i])-65)-(ord(clef[i])-97))%26+65)
        else:
            texte+=chr(((ord(code[i])-97)-(ord(clef[i])-97))%26+97)

    return texte

if __name__ == "__main__":

    # Argparse ain't that hard to use
    # You just need to initialize the ArgumentParser
    # You can use the data in the argument later 
    parser = argparse.ArgumentParser()

    # Then initialize the arguments
    parser.add_argument("--texte", type=str)
    parser.add_argument("--code", type=str)
    parser.add_argument("--key", type=str)

    # and then parse it
    args = parser.parse_args()

    # You can use the data in the argument later
    # you just have to use <nameOfTheVariable>.<nameOfTheArgument>
        
    # If arguments ars set then run once with the data in the args
    if args.texte and args.code:
        print("This ain't good")
    elif args.texte and args.key:
        code = cryptor(args.texte, args.key)
        print(code)
    elif args.code and args.key:
        texte = decryptor(args.code, args.key)
        print(texte)

    else:
        # Else just ask the user if he wants to encrypt decrypt or exit
        end = False

        while end == False:
            reponse = input("What would you like to do ? (E)ncrypt, (D)ecrypt or E(x)it : ")
            if reponse == "x" or reponse == "X":
                end = True
                continue
            elif reponse == "e" or reponse == "E":
                texte = input("You chose to encrypt data\nPlease provide the data : ")
                clef = input("Please provide the key : ")
                bloc = int(input("Please provide the bloc size : "))
                code = cryptor(texte, clef.lower(), bloc)
                print("Encryped data looks like : " + code)
            elif reponse == "d" or reponse == "D":
                code = input("You chose to decrypt data\nPlease provide the data : ")
                clef = input("Please provide the key : ")
                bloc = int(input("Please provide the block size : "))
                texte = decryptor(code, clef.lower(), bloc)
                print("Decrypted data looks like : " + texte)
            else:
                print("That ain't good")
                continue
