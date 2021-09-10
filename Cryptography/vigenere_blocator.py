#!/usr/bin/env python3
import argparse

def cryptor(text, key, bloc):
    
    # bloc spliting
    text_bloc = [ text[i:i+bloc] for i in range(0, len(text), bloc) ]
    code = ""
    print(text_bloc)
    # Loop through the blocs
    for i in range(len(text_bloc)):

        # Loop through each letter of the bloc
        for f in range(len(text_bloc[i])):

            # If the letter is lower case keep the encrypter letter lower case
            if text_bloc[i][f].isupper():
                code+=chr(((ord(text_bloc[i][f])-65)+ (ord(key[f])-97))%26+65)
            else:
                code+=chr(((ord(text_bloc[i][f])-97)+ (ord(key[f])-97))%26+97)

    return code

def decryptor(code, key, bloc):
    
    # Bloc splitting
    code_bloc = [ code[i:i+bloc] for i in range(0, len(code), bloc) ]
    text = ""
   
    # Loop through the blocs
    for i in range(len(code_bloc)):

        # Loop through each letter of the bloc
        for f in range(len(code_bloc[i])):
            if code_bloc[i][f].isupper():
                text+=chr(((ord(code_bloc[i][f])-65)- (ord(key[f])-97))%26+65)
            else:
                text+=chr(((ord(code_bloc[i][f])-97)- (ord(key[f])-97))%26+97)

    return text

if __name__ == "__main__":

    # Argparse ain't that hard to use
    # You just need to initialize the ArgumentParser
    # You can use the data in the argument later 
    parser = argparse.ArgumentParser()

    # Then initialize the arguments
    parser.add_argument("--texte", type=str)
    parser.add_argument("--code", type=str)
    parser.add_argument("--key", type=str)
    parser.add_argument("--bloc", type=int)
    # and then parse it
    args = parser.parse_args()

    # You can use the data in the argument later
    # you just have to use <nameOfTheVariable>.<nameOfTheArgument>
        
    # If arguments ars set then run once with the data in the args
    if args.texte and args.code:
        print("This ain't good")
    elif args.texte and args.key and args.bloc:
        code = cryptor(args.texte, args.key.lower(), args.bloc)
        print(code)
    elif args.code and args.key and args.bloc:
        texte = decryptor(args.code, args.key.lower(), args.bloc)
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
