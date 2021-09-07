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
            code+=chr(((ord(texte[i])-65)+(ord(clef[i])-65))%26+65)
        else:
            code+=chr(((ord(texte[i])-97)+(ord(clef[i])-65))%26+97)

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
            texte+=chr(((ord(code[i])-65)-(ord(clef[i])-65))%26+65)
        else:
            texte+=chr(((ord(code[i])-97)-(ord(clef[i])-65))%26+97)

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
