import forca
import adivinhacao
import nico 
import os
import time as systime

def escolhe_jogo():
    print("*********************************")
    print("*******Escolha o seu jogo!*******")
    print("*********************************")
    print()
    print("(1) Forca (2) Adivinhação (3) Nico's Text Adventure")
    print("Ou digite qualquer valor para sair.")
    print()

    jogo = int(input("Qual jogo? "))

    print()
    if(jogo == 1):
        print("Jogando forca")
        systime.sleep( 3 )
        os.system('cls' if os.name == 'nt' else 'clear')
        forca.jogar()
        escolhe_jogo()
    elif(jogo == 2):
        print("Jogando adivinhação")
        systime.sleep( 3 )
        os.system('cls' if os.name == 'nt' else 'clear')
        adivinhacao.jogar()
        escolhe_jogo()
    elif(jogo == 3):
        print("Jogando Nico's Text Adventure")
        systime.sleep( 3 )
        os.system('cls' if os.name == 'nt' else 'clear')
        nico.jogar()
        escolhe_jogo()

if(__name__ == "__main__"):
    escolhe_jogo()
