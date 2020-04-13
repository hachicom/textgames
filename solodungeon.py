import random, os, math
import time as systime

"""
Rolagem de dados para cada nível.
Indicadores:
0 = poção
1 = ogro (1 d6 ATK)
2 = lobo (2 d6 ATK)
3 = esqueleto (3 d6 ATK)
4 = guerreiro (4 d6 ATK)
5 = morcego (5 d6 ATK)
6 = ciclope (6 d6 ATK)
7 = elfo negro (7 d6 ATK)
8 = lord esqueleto (8 d6 ATK)
9 = mago (9 d6 ATK)
10 = demonio (10 d6 ATK)
11 = Sevla Nanida (9 d6 ATK + 9 d6 DEF)
12 = vazio
13 = tesouro
"""

DUNGEON_DICE = [
    [0, 1, 1, 1, 12, 13] ,
    [1, 2, 12, 12, 12, 13] ,
    [1, 2, 3, 13, 0, 12] ,
    [1, 2, 3, 4, 13, 12] ,
    [2, 3, 4, 5, 13, 12] ,
    [3, 4, 5, 6, 13, 0] ,
    [4, 5, 6, 7, 13, 12] ,
    [5, 6, 7, 8, 13, 12] ,
    [6, 7, 8, 9, 13, 0] ,
    [7, 8, 9, 10, 13, 12] ,
    [11, 11, 11, 11, 11, 11] 
]

"""
PRECOS {objeto, precio}
1 = Escudo de madera     dadoDEF +1 (info[6]++)
2 = pocion               pociones +1 (info[3]++)
3 = escudo de hierro     dadoDEF +2 (info[6] = info[6] + 2)
4 = 3 pociones           pociones +3 (info[3] = info[3] + 3)
5 = espada               dadoATA +1 (info[5]++)
6 = 6 pociones           pociones +6 (info[3] = info[3] + 6)
7 = hacha guerrera       dadoATA +2 (info[5] = info[5] + 2)
8 = armadura con espinas dadoATA +2, dadoDEF +1 (info[5] = info[5] + 2, info[6]++)
9 = armadura magica      dadoDEF +5 (info[6] = info[6] + 5)
"""

PRECOS = [
    [1, 1] ,
    [2, 1] ,
    [3, 2] ,
    [4, 2] ,
    [5, 3] ,
    [6, 3] ,
    [7, 4] ,
    [8, 5] ,
    [9, 6] ,
    [0, -2]
]

def titulo():
    print(" _____")
    print("/  ___|    ")
    print("| |___   ___   _     ____    ")
    print("\___  \ /  _ \| |   /  _ \   ")
    print(" ___| ||  (_) | |__|  (_) |   ")
    print("|_____/ \____/|____|\____/    ")
    print("|  __ \\    ")
    print("| |  | |_   _ _ __   __ _  ___  ___  _ __    ")
    print("| |  | | | | | '_ \\ / _` |/ _ \\/ _ \\| '_ \\    ")
    print("| |__| | |_| | | | | (_| |  __/ (_) | | | |    ")
    print("|_____/ \\__,_|_| |_|\\__, |\\___|\\___/|_| |_|    ")
    print("|   _  \           | |_/ |    ")
    print("|  (_) /  __ _  __ | |__/     ")
    print("|   _  \/ _` |/ __|| '_ \     ")
    print("|  (_) | (_| |\__ \| | | |     ")
    print("|______/\__,_|/___/|_| |_|     \n\n")
    print("v0.6.0 - 2020")
    print("")
    print("Código C original por Cristobal Vasquez")
    print("Adaptado para Python por Adinan Alves")
    print("")
    input('Pressione Enter para jogar.')
    print("")

def mega_salto():
    os.system('cls' if os.name == 'nt' else 'clear')

"""
Esta funcion recibe la fila y la columna a la que el jugador se movera
y el puntero a la posicion (0,0) del tablero. Actualiza el tablero y lo muestra
en pantalla
"""
def mostrar_tablero(fila, columna, tablero):
    #i, j
    print("")
    for i in range(12):
        linha = ""
        for j in range(11):
            if (fila==i and columna==j):
                tablero[i][j] = 74
                linha += ("| {} |".format(chr(tablero[i][j])))
            
            elif (fila+1==i and columna-1==j and (tablero[i][j]<48 or tablero[i][j]==70)):
                linha += ("| 1 |")

            elif (fila+1==i and columna==j and (tablero[i][j]<48 or tablero[i][j]==70)):
                linha += ("| 2 |")

            elif (fila+1==i and columna+1==j and (tablero[i][j]<48 or tablero[i][j]==70)):
                linha += ("| 3 |")

            elif (fila==i and columna+1==j and tablero[i][j]<48):
                linha += ("| 6 |")

            elif (fila-1==i and columna+1==j and tablero[i][j]<48):
                linha += ("| 9 |")

            elif (fila-1==i and columna==j and tablero[i][j]<48):
                linha += ("| 8 |")

            elif (fila-1==i and columna-1==j and tablero[i][j]<48):
                linha += ("| 7 |")

            elif (fila==i and columna-1==j and tablero[i][j]<48):
                linha += ("| 4 |")

            elif (tablero[i][j]==74):
                tablero[i][j] = 88
                linha += ("| {} |".format(chr(tablero[i][j])))
                      
            else:
                if (tablero[i][j] == 58):
                    linha += ("|L10|")

                elif (tablero[i][j] == 48):
                    linha += ("| X |")

                elif (tablero[i][j]>48 and tablero[i][j]<58):
                    linha += ("| L{}|".format(chr(tablero[i][j])))

                else:
                    linha += ("| {} |".format(chr(tablero[i][j])))
                    
        print(linha)
        print("")

def mostrar_stats(info):
    print("\nHP: {}  ATK: {}  DEF: {}\nTesouros: {}  Poções: {}".format(info[7], info[5], info[6], info[4], info[3]))
    
    #print("Escudo: ")
    if(info[0]==1):
        print("Escudo: Escudo de madeira")
    
    elif(info[0]==2):
        print("Escudo: Escudo de ferro")
    
    else:
        print("Escudo: Nenhum")
    
    #print("Arma: ")
    if (info[1]==1):
        print("Arma: Espada")
    
    elif(info[1]==2):
        print("Arma: Machado guerreiro")
    
    else:
        print("Arma: Nenhuma")
    
    #print("Armadura: ")
    if (info[2]==1):
        print("Armadura: Armadura espinhosa")
    
    elif(info[2]==2):
        print("Armadura: Armadura mágica")
    
    else:
        print("Armadura: Nenhuma")

def mostrar_tienda():
    print("              OBJETO                        TESOROS")
    print("(1) ESCUDO DE MADEIRA   (D-DEF +1)             1")
    print("(2) 1 POÇÃO             (POÇÕES +1)            1")
    print("(3) ESCUDO DE FERRO     (D-DEF +2)             2")
    print("(4) 3 POÇÕES            (POÇÕES +3)            2")
    print("(5) ESPADA              (D-ATK +1)             3")
    print("(6) 6 POÇÕES            (POÇÕES +6)            3")
    print("(7) MACHADO GUERREIRO   (D-ATK +2)             4")
    print("(8) ARMADURA ESPINHOSA  (D-ATK +2, D-DEF +1)   5")
    print("(9) ARMADURA MÁGICA     (D-DEF +5)             6")
    print("(0) Não comprar nada\n")

def verificar_movida(fila, columna, tablero, direc):
    dir_int = int(direc)
    mov = [0,0,0]
    
    if (dir_int == 24):
        mov[2] = 42
        
    elif (dir_int == 5):
        mov[2] = 5
    
    elif (dir_int==1):
        if (tablero[fila+1][columna-1]==45 or tablero[fila+1][columna]==70):
            mov[0] = fila + 1
            mov[1] = columna-1
            mov[2] = 1
    
    elif (dir_int==2):
        if (tablero[fila+1][columna]==45 or tablero[fila+1][columna]==70):
            mov[0] = fila + 1
            mov[1] = columna
            mov[2] = 1
            
    elif (dir_int==3): 
        if (tablero[fila+1][columna+1]==45 or tablero[fila+1][columna+1]==70):
            mov[0] = fila + 1
            mov[1] = columna + 1
            mov[2] = 1
    
    elif (dir_int==4):
        if (tablero[fila][columna-1]==45 and fila>0):
            mov[0] = fila
            mov[1] = columna-1
            mov[2] = 1
            
    elif (dir_int==6):
        if (tablero[fila][columna+1]==45 and fila>0):
            mov[0] = fila
            mov[1] = columna + 1
            mov[2] = 1
    
    elif (dir_int==7 and fila>0):
        if (tablero[fila-1][columna-1]==45):
            mov[0] = fila - 1
            mov[1] = columna - 1
            mov[2] = 1
    
    elif (dir_int==8 and fila>0):
        if (tablero[fila-1][columna]==45):
            mov[0] = fila - 1
            mov[1] = columna
            mov[2] = 1
    
    elif (dir_int==9 and fila>0):
        if (tablero[fila-1][columna+1]==45):
            mov[0] = fila - 1
            mov[1] = columna + 1
            mov[2] = 1
    else:
        mov[2] = 0
    
    return mov
    
    
def verificar_encierro(fila, columna, tablero):
    if (tablero[fila+1][columna-1]!=45 and tablero[fila+1][columna]!=45 
    and tablero[fila+1][columna+1]!=45 and tablero[fila][columna+1]!=45 
    and tablero[fila-1][columna+1]!=45 and tablero[fila-1][columna]!=45 
    and tablero[fila-1][columna-1]!=45 and tablero[fila][columna-1]!=45):
        if (tablero[fila+1][columna-1]==70 or tablero[fila+1][columna]==70 or tablero[fila+1][columna+1]==70):
            return 0
        else:
            return 1
    else:
        return 0

def mostrar_dado(dado):
    if (dado==1):
        print(" _________ ")
        print("|         |")
        print("|         |")
        print("|    O    |")
        print("|         |")
        print("|_________|")

    elif (dado==2):
        print(" _________ ")
        print("|         |")
        print("| O       |")
        print("|         |")
        print("|       O |")
        print("|_________|")

    elif (dado==3):
        print(" _________ ")
        print("|         |")
        print("| O       |")
        print("|    O    |")
        print("|       O |")
        print("|_________|")

    elif (dado==4):
        print(" _________ ")
        print("|         |")
        print("| O     O |")
        print("|         |")
        print("| O     O |")
        print("|_________|")

    elif (dado==5):
        print(" _________ ")
        print("|         |")
        print("| O     O |")
        print("|    O    |")
        print("| O     O |")
        print("|_________|")

    elif (dado==6):
        print(" _________ ")
        print("|         |")
        print("| O     O |")
        print("| O     O |")
        print("| O     O |")
        print("|_________|")

    return 0

def batalla(cont_casilla, items):
    dados_def_enemigo = 0
    dados_ata_enemigo = cont_casilla
    hp_enemigo = 1
    golpes_enemigo = 0
    defensa_enemigo = 0
    defensa = 0 
    golpes = 0 
    i=0
    
    if (cont_casilla==1):
        enemigo = "Ogro"
    
    elif (cont_casilla==2):
        enemigo = "Lobo" 
    
    elif (cont_casilla==3):
        enemigo = "Esqueleto" 
    
    elif (cont_casilla==4):
        enemigo = "Guerreiro" 
    
    elif (cont_casilla==5):
        enemigo = "Morcego" 
    
    elif (cont_casilla==6):
        enemigo = "Ciclope" 
    
    elif (cont_casilla==7):
        enemigo = "Elfo Negro" 
    
    elif (cont_casilla==8):
        enemigo = "Lord Esqueleto" 
    
    elif (cont_casilla==9):
        enemigo = "Mago" 
    
    elif (cont_casilla==10):
        enemigo = "Demonio" 
    
    else:
        enemigo = "Sevla Nanida" 
        dados_ata_enemigo = 9
        dados_def_enemigo = 9
    
    print("Resultado: {} aparece disposto a te atacar!\n".format(enemigo)) #, end = ''
    if (cont_casilla==11):
        print("Finalmente você encontrou o temido feiticeiro Sevla Nanida!\nChegou a hora da batalha final!")
        
    input("Pressione ENTER para continuar")
    mega_salto()    

    while (hp_enemigo>0 and items[7]>0):
        for i in range(dados_ata_enemigo):
            dados = random.randrange(1,7) #D6
            if (dados==6):
                golpes_enemigo+=1
                    
        
        if (golpes_enemigo>0):
            input("\n{} ataca com {} golpe(s)!\nHora de lançar seus DADOS DE DEFESA.\n\nPresiona enter...".format(enemigo,golpes_enemigo))
            mega_salto()
            
            j = 0
            for j in range(items[6]):
                dados = random.randrange(1,7) #D6
                mostrar_dado(dados)
                if (dados==6):
                    defensa+=1
                
            
            golpes_enemigo = golpes_enemigo - defensa
            if (golpes_enemigo<0):
                golpes_enemigo = 0
            
            if (golpes_enemigo==0):
                print("\nVocê esquiva com sucesso!")
            
            elif(golpes_enemigo==1):
                items[7]-=1
                print("{} consegue lhe causar 1 pt de dano!".format(enemigo))
            
            else:
                items[7] = items[7] - golpes_enemigo
                if (items[7]<0):
                    items[7] = 0
                
                print("{} consegue lhe causar {} pts de dano!".format(enemigo, golpes_enemigo))
        
        else:
            print("\n{} ataca, mas falha em lhe acertar.".format(enemigo))
        
        mostrar_stats(items)
        
        if (items[7]==0):
            print("\nSeus sentidos começam a ceder com a perda de sangue, e você cai no chão.\n")
            input("Pressione ENTER...")
            return 2
        
        else:
            if (items[7]<6):
                print("\nVocê sente que suas feridas estão se agravando...cuidado...")
            
            input("\nHora de lançar seus DADOS DE ATAQUE.\n\nPresiona enter...")
            mega_salto()
            
            for i in range(items[5]):
                dados = random.randrange(1,7) #D6
                mostrar_dado(dados)
                if (dados==6):
                    golpes+=1
                
            
            for i in range(dados_def_enemigo):
                dados = random.randrange(1,7) #D6
                if (dados==6):
                    defensa_enemigo+=1
                
            
            if (golpes==0):
                print("\nVocê ataca, mas erra miseravelmente.")
            
            else:
                golpes = golpes - defensa_enemigo
                if (golpes<0):
                    golpes = 0
                
                if (golpes==0):
                    print("\n{} esquiva seus ataques com facilidade".format(enemigo))
                
                elif (golpes==1):
                    hp_enemigo-=1
                    if (items[1]==1):
                        print("\nVocê agita sua espada e corta o inimigo ao meio. {} está morto".format(enemigo))
                    
                    elif(items[1]==2):
                        print("\nVocê lança seu machado, cravando na cabeça do inimigo. {} está morto".format(enemigo))
                    
                    else:
                        print("\nVocê acerta um soco devastador na cabeça do inimigo. {} está morto".format(enemigo))
                    
                else:
                    hp_enemigo-=1
                    print("\nVocê lança toda sua fúria no inimigo")
                    print("\nCom uma sequência devastadora, {} já não está mais entre nós...".format(enemigo))
                
        mostrar_stats(items)
        input("Pressione ENTER para continuar")
        mega_salto()    
        
        defensa_enemigo = 0
        defensa = 0
        golpes_enemigo = 0
        golpes = 0
    
    if (cont_casilla==11):
        return 3
    
    return 0


def beber_pocion(items, max_hp):
    mega_salto()
    if (items[7]==max_hp or items[3]==0):
        input("\nNão pode beber poções no momento.\n(Presiona enter para continuar...)")
        mega_salto()
        return 0
    
    i = 0
    while (items[7]!=max_hp and items[3]!=0):
        if (i==0):
            print("\nDeseja beber uma poção para recuperar 1 ponto de vida?")
            print("\n(Pontos de vida: {} | Poções: {})".format(items[7], items[3]))
            respuesta = input("\n(1) Sim\n(2) Não\nComando: ")
        
        else:
            print("\nDeseja beber outra?\n(Pontos de vida: {} | Poções: {})".format(items[7], items[3]))
            respuesta = input("\n(1) Sim\n(2) Não\nComando: ")
        
        while respuesta not in ['1','2']:
            respuesta = input("\nDigite uma opção válida (1 ou 2): ")

        if (respuesta == '1'):
            items[7]+=1
            items[3]-=1
            print("\nVocê bebeu uma poção e recuperou 1 ponto de vida.")
        
        else:
            return 0
        
        if (items[7]==max_hp or items[3]==0):
            input("\nNão pode beber poções no momento.\n(Presiona enter para continuar...)")
            mega_salto()
            return 0
        
    i+=1
    return 0

def comprar(items):
    mega_salto()
    if (items[4]==0):
        input("\nNão tem tesouros para usar na loja.\n(Pressiona enter para continuar....)")
        mega_salto()
        return 0

    i = 0
    while(items[4]>0):
        if (i==0):
            print("\nDeseja visitar a loja?")
            respuesta = input("\n(Tesoros: {})\n(1) Sim\n(2) Passo\nComando: ".format(items[4]))
        
        else:
            print("\nAinda tem tesouros ({}), deseja comprar algo mais?".format(items[4]))
            respuesta = input("\n(1) Sim\n(2) Passo\n: ")
            
        while (respuesta not in ('1','2')):
            respuesta = input("\nDigite uma opção válida (1 ou 2): ")
        
        if (respuesta == '1'):
            
            mostrar_tienda()
            mostrar_stats(items)
            respuesta = input("\nO que deseja comprar? ")
            
            while (int(respuesta) not in [0,1,2,3,4,5,6,7,8,9] or items[4] < PRECOS[int(respuesta)][1]):
                respuesta = input("\nDigite uma opção válida (0 a 9): ")
            
            if (int(respuesta) == 0):
                return 0
            
            elif (int(respuesta)==1):
                if (items[0]==1):
                    print("\nJá tem este escudo")
                
                elif (items[0]==2):
                    print("\nJá tem escudo melhor")
                
                else:
                    items[0] = 1
                    items[6]+=1
                    items[4]-=1
                    print("\nEscudo de madeira adquirido")
                
            
            elif (int(respuesta)==2):
                items[3]+=1
                items[4]-=1
                print("\nPoção adquirida")
            
            elif (int(respuesta)==3):
                if (items[0]==2):
                    print("\nJá tem este escudo")
                
                elif (items[0]==1):
                    items[0] = 2
                    items[6] = items[6] + 1
                    items[4] = items[4] - 2
                    print("\nEscudo de ferro adquirido")
                
                else:
                    items[0] = 2
                    items[6] = items[6] + 2
                    items[4] = items[4] - 2
                    print("\nEscudo de ferro adquirido")
                
            
            elif (int(respuesta)==4):
                items[3] = items[3] + 3
                items[4] = items[4] - 2
                print("\n3 poções adquiridas")
            
            elif (int(respuesta)==5):
                if (items[1]==1):
                    print("\nJá tem esta arma")
                
                elif (items[1]==2):
                    print("\nJá tem arma melhor")
                
                else:
                    items[1] = 1
                    items[5]+=1
                    items[4] = items[4] - 3
                    print("\nEspada adquirida")
                
            
            elif (int(respuesta)==6):
                items[3] = items[3] + 6
                items[4] = items[4] - 3
                print("\n6 poções adquiridas")
            
            elif (int(respuesta)==7):
                if (items[1]==2):
                    print("\nJá tem esta arma")
                
                elif(items[1]==1):
                    items[1] = 2
                    items[5] = items[5] + 1
                    items[4] = items[4] - 4
                    print("\nMachado guerreiro adquirido")
                
                else:
                    items[1] = 2
                    items[5] = items[5] + 2
                    items[4] = items[4] - 4
                    print("\nMachado guerreiro adquirido")
                
            
            elif(int(respuesta)==8):
                if (items[2]==1 or items[2]==3):
                    print("\nJá tem esta armadura")
                
                elif(items[2]==4):
                    print("\nJá tem esta armadura no inventário, deseja equipar?")
                    equipar = input("\n(1) Sim\n(2) Não\nComando: ")
                    
                    while (equipar != '1' or equipar != '2'):
                        equipar = input("\nDigite uma opção válida (1 ou 2): ")
                    
                    if (equipar == '1'):
                        items[2] = 3
                        items[5] = items[5] + 2
                        items[6] = items[6] - 4
                        print("\nArmadura espinhosa equipada. A outra armadura foi guardada no inventário")
                    
                
                elif(items[2]==2):
                    items[2] = 3
                    items[5] = items[5] + 2
                    items[6] = items[6] + 1
                    items[4] = items[4] - 5
                    print("\nArmadura espinhosa adquirida e equipada")
                
                else:
                    items[2] = 1
                    items[5] = items[5] + 2
                    items[6] = items[6] + 1
                    items[4] = items[4] - 5
                    print("\nArmadura espinhosa adquirida e equipada")
                
            
            else:
                if (items[2]==2 or items[2]==4):
                    print("\nJá tem esta armadura")
                
                elif(items[2]==3):
                    print("\nJá tem esta armadura no inventário, deseja equipar?")
                    equipar = input("\n(1) Sim\n(2) Não\nComando: ")
                    
                    while (equipar != '1' or equipar != '2'):
                        equipar = input("\nDigite uma opção válida (1 ou 2): ")
                        
                    if (equipar == '1'):
                        items[2] = 4
                        items[5] = items[5] - 2
                        items[6] = items[6] + 4
                        print("\nArmadura mágica equipada. A outra armadura foi guardada no inventário")
                    
                
                elif(items[2]==1):
                    items[2] = 4
                    items[6] = items[6] + 5
                    items[4] = items[4] - 6
                    print("\nArmadura mágica adquirida e equipada")
                
                else:
                    items[2] = 2
                    items[6] = items[6] + 5
                    items[4] = items[4] - 6
                    print("\nArmadura mágica adquirida e equipada")
                

        else:
            mega_salto()
            return 0
        
        if (items[4]==0):
            input("\nNão tem mais tesouros.\n(Pressiona enter para continuar....)")
            mega_salto()
            return 0
        
        i+=1
    


def dificultad(dif):
    modo = int(dif)
    items = [0,0,0,0,0,0,0,0]
    
    if (modo==1):
        items[3] = 6 #pocoes
        items[4] = 4 #tesouro
        items[5] = 4 #d6 ATK
        items[6] = 4 #d6 DEF
        items[7] = 23 #HP
    
    elif (modo==2):
        items[3] = 3
        items[4] = 2
        items[5] = 2
        items[6] = 2
        items[7] = 20
    
    elif (modo==3):
        items[3] = 0
        items[4] = 0
        items[5] = 1
        items[6] = 1
        items[7] = 17
        
    return items
    

"""
Função Principal
"""
def jogar():
    estado = 0                         # 0 = jugando, 1 = encerrado, 2 = muerto, 3 = victoria, 42 = salir 
    movimento = [0,0]
    info = [0,0,0,0,0,0,0,0]
    tablero = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
    
    nivel = 48                       # fila atual
    filaA = 0                        # coluna atual                        
    columnaA = 5

    mega_salto()
    titulo()
    print("\nDificuldade:\n(1) Nutella\n(2) Aventureiro\n(3) Lenda")
    modo = input("\nSelecione a dificuldade do jogo: ")
    while (modo not in ('1','2','3')):
        modo = input("\nDigite uma opção válida (1, 2 ou 3): ")
        
    info = dificultad(modo)
        
    print("\nTabuleiro:\n(1) Clássico\n(2) Entrada Aleatória")
    tipoTabuleiro = input("\nSelecione a opção: ")
    while (tipoTabuleiro not in ('1','2')):
        tipoTabuleiro = input("\nDigite uma opção válida (1 ou 2): ")
        
    if tipoTabuleiro == "2":
        columnaA = random.randrange(1,10)
    
    mega_salto()
    print("\n\nWELCOME TO SOLO DUNGEON BASH\nVocê depara com uma caverna sombria.")
    print("Lá dentro se encontra Sevla Nanida, um feiticeiro que cria monstros para aterrorizar seu vilarejo há anos.")
    print("Não suportando mais a situação, você decide enfrentar a caverna onde o mago se esconde com suas criaturas")
    print("para derrotá-lo e restaurar a paz.")
    print("")
    print("Boa sorte, o vilarejo conta com você!\n")
    input("Pressione ENTER para continuar...")
    mega_salto()
    
    i = 0
    j = 0
    for i in range(12):
        for j in range(11):
            if (i==filaA and j==columnaA):
                tablero[i][j] = 74
            
            elif (i==11 and j==5):
                tablero[i][j] = 70
            
            elif (i==0 or i==11 or j==10):
                tablero[i][j] = 88
            
            elif (j==0):
                tablero[i][j] = nivel
            
            else:
                tablero[i][j] = 45
                    
        nivel+=1

    resultado = ""
    dado = 0
    
    while (estado==0):    
        mega_salto()
        mostrar_tablero(filaA, columnaA, tablero)
        mostrar_stats(info)
        mostrar_dado(dado)
        print("")
        print(resultado)
        print("")
        direccion = input("Digite um número para se locomover, 5 para beber poção e/ou compras: ")
        
        while (tipoTabuleiro not in ('1','2','3','4','5','6','7','8','9','24')):
            tipoTabuleiro = input("\nDigite uma opção válida (1 à 9): ")
        
        movimento = verificar_movida(filaA, columnaA, tablero, direccion);
        if (movimento[2]==1):
            filaA = movimento[0]
            columnaA = movimento[1]
            dado = random.randrange(1,7) #D6
            contenidoCasilla = DUNGEON_DICE[filaA-1][dado-1]
                        
            if (contenidoCasilla==0):
                info[3]+=1
                resultado = ("Resultado: Poções +1")
            
            elif (contenidoCasilla==13):
                info[4]+=1
                resultado = ("Resultado: Tesouros +1")
            
            elif (contenidoCasilla==12):
                resultado = ("Resultado: Nada por aqui, caminho livre")
            
            else:
                mega_salto()
                mostrar_tablero(filaA, columnaA, tablero)
                mostrar_stats(info)
                mostrar_dado(dado)
                print("")
                estado = batalla(contenidoCasilla, info)
                resultado = ""
            
            if (filaA!=11 and estado!=2):
                estado = verificar_encierro(filaA, columnaA, tablero)
                    
        elif (movimento[2]==5):
            beber_pocion(info, 26-(int(modo)*3))
            comprar(info)
            
        elif (movimento[2]==42):
            estado = 42
        
        else:
            resultado = ("Resultado: Movimento inválido")
            

    if (estado==1):
        mega_salto()
        print("\n\nVocê se perde no calabouço, em meio à escuridão\n")
        print("Não demora muito para sentir um bafo quente e vivo em sua direção\n");
        print("\nOh não! Você foi devorado por um Grue!\n")
    
    elif (estado==2):
        mega_salto()
        print("\n\nCom tantos ferimentos, só lhe resta aguardar o fim.\n")
        print("Seu inimigo assiste enquanto sua vida abandona aos poucos o seu corpo mortal\n")
        print("\nAo menos morreu tentando, mas infelizmente Sevla Nanida continuará atormentando seu vilarejo\n")
    
    elif (estado==3):
        mega_salto()
        print("\nAos seus pés está o corpo de Sevla Nanida.\n")
        print("Você sai da caverna com os pertences do falecido tirano como prova.")
        print("Ao chegar no vilarejo, todos festejam o seu retorno e a sua vitória.\n")
        print("\nSeu nome e ato heróico vão inspirar canções e poemas por muitas gerações!\n")
        print("")
        print("\nParabéns! Você venceu esta partida de Solo Dungeon Bash!\n")
    
    elif(estado==42):
        mega_salto()
        print("\n\nvocê decide cair fora desta situação")
        print("há aventuras bem melhores do que um dungeon crawler em texto\n")
        print("\nseria melhor ter ido ver o filme do Pelé\n")

    input("GAME OVER\n\nPressiona ENTER para sair...")
    
    mega_salto()
    return 0

'''
Start game
'''
if __name__ == '__main__':
    jogar()