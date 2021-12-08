## IMPORTAION MODULES ##

from math import *
from random import *
from numpy import random as nprd


## INITIALISATIONS DIVERSES ##

def paquet():
    return [
        'as de trefle', 'as de carreau', 'as de coeur', 'as de pic',
        '2 de trefle', '2 de carreau', '2 de coeur', 'as de pic',
        '3 de trefle', '3 de carreau', '3 de coeur', '3 de pic',
        '4 de trefle', '4 de carreau', '4 de coeur', '4 de pic',
        '5 de trefle', '5 de carreau', '5 de coeur', '5 de pic',
        '6 de trefle', '6 de carreau', '6 de coeur', '6 de pic',
        '7 de trefle', '7 de carreau', '7 de coeur', '7 de pic',
        '8 de trefle', '8 de carreau', '8 de coeur', '8 de pic',
        '9 de trefle', '9 de carreau', '9 de coeur', '9 de pic',
        '10 de trefle', '10 de carreau', '10 de coeur', '10 de pic',
        'valet de trefle', 'valet de carreau', 'valet de coeur', 'valet de pic',
        'dame de trefle', 'dame de carreau', 'dame de coeur', 'dame de pic',
        'roi de trefle', 'roi de carreau', 'roi de coeur', 'roi de pic'
    ]


ValCartes = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'valet': 10,
    'dame': 10,
    'roi': 10
}


def initPioche(n):
    pioche = []
    cartes = paquet()
    for i in range(n):
        pioche.extend(cartes)
    shuffle(pioche)
    return pioche


def initJoueurs(GDict, n):
    for i in range(n):
        GDict['joueurs'][i] = {}
        GDict['joueurs'][i]['nom'] = input('Nom du joueur '+str(i+1)+' : ')
        while True:
            try:
                typ = int(input('Humain (0) ou ordinateur (1) : '))
            except:
                print("Entrez une valeur correcte")
                continue
            if typ != 0 and typ != 1:
                print("Entrez une valeur correcte")
                continue
            else:
                break
        GDict['joueurs'][i]['type'] = typ
        GDict['joueurs'][i]['ingame'] = True
        GDict['joueurs'][i]['blackjack'] = False
        GDict['joueurs'][i]['burst'] = False


def initData(GDict, valeur, v=0):
    for i in GDict['joueurs']:
        GDict['joueurs'][i][valeur] = v
    GDict['croupier'][valeur] = v


def initVictoires(GDict):
    for i in GDict['joueurs']:
        GDict['victoires'][GDict['joueurs'][i]['nom']] = 0


## FONCTIONS DE JEU ##

def valeurCartes(carte, score):
    carte_WO_couleur = carte.split()[0]
    if carte_WO_couleur == 'as':
        return valeurAs(score)
    else:
        return ValCartes[carte_WO_couleur]


def valeurAs(score):
    if score+11 <= 21:
        return 11
    else:
        return 1


def piocheCarte(p, x=1):
    piochees = []
    for i in range(x):
        piochees.append(p.pop(0))
    return piochees


def gagnants(GDict):
    gagnants = []
    for j in GDict['joueurs']:
        if GDict['joueurs'][j]['burst']:
            continue
        elif GDict['croupier']['burst']:
            gagnants.append(j)
        elif GDict['joueurs'][j]['score'] >= GDict['croupier']['score']:
            gagnants.append(j)
    return gagnants

def gain(j, GDict):

    mise = GDict['joueurs'][j]['mise']

    # cas où je joueur dépasse 21
    if GDict['joueurs'][j]['burst']: 
        GDict['croupier']['wallet'] += mise
        
    # cas où le croupier dépasse 21
    elif GDict['croupier']['burst']:
        if GDict['joueurs'][j]['blackjack']:
            GDict['joueurs'][j]['wallet'] += 2.5 * mise
            GDict['croupier']['wallet'] -= 1.5 * mise
        else:
            GDict['joueurs'][j]['wallet'] += 2 * mise
            GDict['croupier']['wallet'] -= mise

    # cas où le croupier fait blackjack
    elif GDict['croupier']['blackjack']:
        if GDict['joueurs'][j]['blackjack']:
            GDict['joueurs'][j]['wallet'] += 2 * mise
            GDict['croupier']['wallet'] -= mise
        else:
            GDict['croupier']['wallet'] += mise

    # cas où le croupier fait un score ≤ 21
    else:
        if GDict['joueurs'][j]['blackjack']:
            GDict['joueurs'][j]['wallet'] += 2.5 * mise
            GDict['croupier']['wallet'] -= 1.5 * mise
        elif GDict['joueurs'][j]['score'] > GDict['croupier']['score']:
            GDict['joueurs'][j]['wallet'] += 2 * mise
            GDict['croupier']['wallet'] -= mise
        elif GDict['joueurs'][j]['score'] == GDict['croupier']['score']:
            GDict['joueurs'][j]['wallet'] += mise
        else:
            GDict['croupier']['wallet'] += mise
    
    GDict['joueurs'][j]['mise'] = 0
       


## CHOIX DE PIOCHER ##

def continueHuman(j, GDict):
    c = ''
    while c != 'o' and c != 'n':
        c = str(input('Piocher ? (o/n) : '))
    if c == 'o':
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")


def continueAlea(j,GDict):
    if choice([False, True]):
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")


def continuePara(j,GDict,p=0.5):
    if nprd.choice([False, True], p=[1-p, p]):
        GDict['joueurs'][j]['ingame'] = True
    else:
        GDict['joueurs'][j]['ingame'] = False
        print(GDict['joueurs'][j]['nom'], "ne pioche pas")

def continueIntel(j,GDict):
    if GDict['joueurs'][j]['score'] <= 10:
        p = 1
    elif GDict['joueurs'][j]['score'] < 21:
        p = 1-((GDict['joueurs'][j]['score']-11)/10)
    else:
        p = 0
    continuePara(j,GDict,p)


def continueCroupier(GDict):
    if GDict['croupier']['score'] < 17:
        GDict['croupier']['ingame'] = True
    else:
        GDict['croupier']['ingame'] = False
        print("\nLe croupier ne pioche pas")


## CHOIX DE MISE ##

def miseAlea(j,Gdict):
    return randint(1,floor(Gdict['joueurs'][j]['wallet']))


## FONCTIONS DE DÉROULEMENT ##

def premierTour(GDict):
    print("\n\nPremier tour:")
    usrToDel = []
    for i in GDict['joueurs']:

        if GDict['joueurs'][i]['ingame'] and not GDict['joueurs'][i]['type']:
            print("\nJoueur :", GDict['joueurs'][i]['nom'])
            if GDict['joueurs'][i]['wallet'] <= 0:
                print("Vous n'avez plus d'OtterCoins, vous ne pouvez plus jouer")
                usrToDel.append(i)
            else:
                print(
                    f"Combien voulez-vous miser ? ({GDict['joueurs'][i]['wallet']} OtterCoins restants) : ", end='')
                while True:
                    try:
                        mise = int(input())
                    except:
                        print("Entrez une valeur correcte")
                        continue
                    if mise > GDict['joueurs'][i]['wallet']:
                        print("Vous devez miser une valeur ≤ à votre portefeuille")
                    else:
                        break
                GDict['joueurs'][i]['wallet'] -= mise
                GDict['joueurs'][i]['mise'] += mise
            cartes2 = piocheCarte(GDict['pioche'], 2)
            print("Main du joueur :", cartes2)
            for j in cartes2:
                GDict['joueurs'][i]['score'] += valeurCartes(
                    j, GDict['joueurs'][i]['score'])
            print("Score actuel :", GDict['joueurs'][i]['score'])
            if GDict['joueurs'][i]['score'] == 21:
                GDict['joueurs'][i]['blackjack'] = True
                GDict['joueurs'][i]['ingame'] = False

        elif GDict['joueurs'][i]['ingame'] and GDict['joueurs'][i]['type']:
            print("\nJoueur :", GDict['joueurs'][i]['nom'])
            if GDict['joueurs'][i]['wallet'] <= 0:
                usrToDel.append(i)
            else:
                mise = miseAlea(i,GDict)
                GDict['joueurs'][i]['wallet'] -= mise
                GDict['joueurs'][i]['mise'] += mise
                print(GDict['joueurs'][i]['nom'], "mise", mise, "OtterCoins")
            cartes2 = piocheCarte(GDict['pioche'], 2)
            print("Main du joueur :", cartes2)
            for j in cartes2:
                GDict['joueurs'][i]['score'] += valeurCartes(j, GDict['joueurs'][i]['score'])
            print("Score actuel :", GDict['joueurs'][i]['score'])
            if GDict['joueurs'][i]['score'] == 21:
                GDict['joueurs'][i]['blackjack'] = True
                GDict['joueurs'][i]['ingame'] = False

    for i in usrToDel:
        del GDict['joueurs'][i]

    if GDict['croupier']['ingame']:
        cartes2 = piocheCarte(GDict['pioche'], 2)
        for j in cartes2:
            GDict['croupier']['score'] += valeurCartes(
                j, GDict['croupier']['score'])
        print("\nScore du croupier :", GDict['croupier']['score'])
        if GDict['croupier']['score'] == 21:
            GDict['croupier']['blackjack'] = True
            GDict['croupier']['ingame'] = False



def tourJoueur(j, GDict):

    if GDict['joueurs'][j]['ingame'] and not GDict['joueurs'][j]['type']:

        print("\nJoueur :", GDict['joueurs'][j]['nom'])
        print('Score partie :', GDict['joueurs'][j]['score'])
        continueHuman(j, GDict)
        while GDict['joueurs'][j]['ingame']:
            carte = piocheCarte(GDict['pioche'])[0]
            val = valeurCartes(carte, GDict['joueurs'][j]['score'])
            print("Vous avez pioché :", carte, "(valeur : "+str(val)+")")
            GDict['joueurs'][j]['score'] += val
            print("Votre score est donc de :", GDict['joueurs'][j]['score'])
            if GDict['joueurs'][j]['score'] == 21:
                GDict['joueurs'][j]['ingame'] = False
            elif GDict['joueurs'][j]['score'] > 21:
                print("Vous avez dépassé 21 ! Perdu !")
                GDict['joueurs'][j]['ingame'] = False
                GDict['joueurs'][j]['burst'] = True
            else:
                continueHuman(j, GDict)

    elif GDict['joueurs'][j]['ingame'] and GDict['joueurs'][j]['type']:
        print("\nJoueur :", GDict['joueurs'][j]['nom'])
        print('Score partie: ', GDict['joueurs'][j]['score'])
        continueIntel(j,GDict)
        while GDict['joueurs'][j]['ingame']:
            carte = piocheCarte(GDict['pioche'])[0]
            val = valeurCartes(carte, GDict['joueurs'][j]['score'])
            GDict['joueurs'][j]['score'] += val
            print("Nouveau score :", GDict['joueurs'][j]['score'])
            if GDict['joueurs'][j]['score'] == 21:
                GDict['joueurs'][j]['ingame'] = False
            elif GDict['joueurs'][j]['score'] > 21:
                print(GDict['joueurs'][j]['nom'], "a dépassé 21 ! Perdu !")
                GDict['joueurs'][j]['ingame'] = False
                GDict['joueurs'][j]['burst'] = True
            else:
                continueIntel(j,GDict)



def tourComplet(GDict):
    print()
    for j in GDict['joueurs']:
        tourJoueur(j,GDict)
    continueCroupier(GDict)
    while GDict['croupier']['ingame']:
        carte = piocheCarte(GDict['pioche'])[0]
        val = valeurCartes(carte, GDict['croupier']['score'])
        GDict['croupier']['score'] += val
        print("\nScore du croupier :", GDict['croupier']['score'])
        if GDict['croupier']['score'] == 21:
            GDict['croupier']['ingame'] = False
        elif GDict['croupier']['score'] > 21:
            print("Le croupier a dépassé !")
            GDict['croupier']['ingame'] = False
            GDict['croupier']['burst'] = True
        else:
            continueCroupier(GDict)



def partieComplete(GDict):
    tourComplet(GDict)

    print("\n\nPartie terminée")
    victorieux = gagnants(GDict)

    for j in GDict['joueurs']:
        gain(j,GDict)

    print("Résumé de la partie :")
    usrToDel = []
    for j in GDict['joueurs']:
        if GDict['joueurs'][j]['wallet'] < 1:
            usrToDel.append(j)
        GDict['victoires'][GDict['joueurs'][j]['nom']] += 1
        if j in victorieux:
            print("-",GDict['joueurs'][j]['nom'],":",GDict['joueurs'][j]['score'], "gagné →", GDict['joueurs'][j]['wallet'],"OtterCoins")
        else:
            print("-",GDict['joueurs'][j]['nom'],":",GDict['joueurs'][j]['score'], "perdu →", GDict['joueurs'][j]['wallet'],"OtterCoins")
    print("- Croupier", GDict['croupier']['score'], "→", GDict['croupier']['wallet'],"OtterCoins")
    for j in usrToDel:
        del GDict['joueurs'][j]



def voulezVousPartir(GDict):
    print()
    if len(GDict['joueurs']) <= 0:
        print("Il n'y a plus de joueurs en jeu, vous ne pouvez rejoueur.")
        return
    else:
        usrToDel = []
        for j in GDict['joueurs']:
            if not GDict['joueurs'][j]['type']:
                strAff = GDict['joueurs'][j]['nom']+", voulez vous partir ? (o/n) "
                rep = ''
                while rep != 'o' and rep != 'n':
                    rep = input(strAff)
                if rep == 'o':
                    usrToDel.append(j)
        for j in usrToDel:
            del GDict['joueurs'][j]
