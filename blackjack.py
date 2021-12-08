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


def initJoueurs(JDict, n):
    for i in range(n):
        JDict['joueurs'][i] = {}
        JDict['joueurs'][i]['nom'] = input('Nom du joueur '+str(i+1)+' : ')
        while True:
            try:
                typ = int(input('Humain (0) ou ordinateur (1) : '))
            except:
                print("Entrez une valeur correcte")
                continue
            if typ != 0 and typ != 1:
                continue
            else:
                break
        JDict['joueurs'][i]['type'] = typ
        JDict['joueurs'][i]['ingame'] = True
        JDict['joueurs'][i]['blackjack'] = False
        JDict['joueurs'][i]['burst'] = False


def initScores(JDict, valeur, v=0):
    for i in JDict['joueurs']:
        JDict['joueurs'][i][valeur] = v
    JDict['croupier'][valeur] = v


def initVictoires(JDict):
    for i in JDict['joueurs']:
        JDict['victoires'][JDict['joueurs'][i]['nom']] = 0
    JDict['victoires']['croupier'] = 0


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


def gagnants(JDict):
    gagnants = []
    for j in JDict['joueurs']:
        if JDict['joueurs'][j]['burst']:
            continue
        if JDict['joueurs'][j]['blackjack']:
            gagnants.append(j)
        elif JDict['joueurs'][i]['score'] >= JDict['croupier']['score']:
            gagnants.append(j)
    return gagnants


## CHOIX DE PIOCHER ##

def continueHuman(j, JDict):
    c = ''
    while c != 'oui' and c != 'non':
        c = str(input('Piocher ? (oui / non) : '))
    if c == 'oui':
        JDict['joueurs'][j]['ingame'] = True
    else:
        JDict['joueurs'][j]['ingame'] = False
        print(JDict['joueurs'][j]['nom'], "ne pioche pas")


def continueAlea(j,JDict):
    if choice([False, True]):
        JDict['joueurs'][j]['ingame'] = True
    else:
        JDict['joueurs'][j]['ingame'] = False
        print(JDict['joueurs'][j]['nom'], "ne pioche pas")


def continuePara(j,JDict,p=0.5):
    if nprd.choice([False, True], p=[1-p, p]):
        JDict['joueurs'][j]['ingame'] = True
    else:
        JDict['joueurs'][j]['ingame'] = False
        print(JDict['joueurs'][j]['nom'], "ne pioche pas")

def continueIntel(j,JDict):
    if JDict['joueurs'][j]['score'] <= 10:
        p = 1
    elif JDict['joueurs'][j]['score'] < 21:
        p = 1-((JDict['joueurs'][j]['score']-11)/10)
    else:
        p = 0
    continuePara(p)


def continueCroupier(JDict):
    if JDict < 17:
        JDict['croupier']['ingame'] = True
    else:

        JDict['croupier']['ingame'] = False
        print("Le croupier ne pioche pas")


## CHOIX DE MISE ##

def choixMise(score):
    if score <= 10:
        p = score/10
    elif score < 21:
        p = 1-((score-11)/10)
    elif score == 21:
        p = 1
    return p


## FONCTIONS DE DÉROULEMENT ##

def premierTour(JDict):
    print("\n\nPremier tour:")
    usrToDel = []
    for i in JDict['joueurs']:

        if JDict['joueurs'][i]['ingame'] and not JDict['joueurs'][i]['type']:

            print("\nJoueur :", JDict['joueurs'][i]['nom'])

            if JDict['joueurs'][i]['wallet'] <= 0:
                print("Vous n'avez plus d'OtterCoins, vous ne pouvez plus jouer")
                usrToDel.append(i)
            else:
                print(
                    f"Combien voulez-vous miser ? ({JDict['joueurs'][i]['wallet']} OtterCoins restants) : ", end='')
                while True:
                    try:
                        mise = int(input())
                    except:
                        print("Entrez une valeur correcte")
                        continue
                    if mise > JDict['joueurs'][i]['wallet']:
                        print("Vous devez miser une valeur ≤ à votre portefeuille")
                    else:
                        break
                JDict['joueurs'][i]['wallet'] -= mise
                JDict['joueurs'][i]['mise'] += mise
            
            cartes2 = piocheCarte(JDict['pioche'], 2)
            print("Main du joueur : ", cartes2)
            for j in cartes2:
                JDict['joueurs'][i]['score'] += valeurCartes(
                    j, JDict['joueurs'][i]['score'])
            print("Score actuel :", JDict['joueurs'][i]['score'])
            if JDict['joueurs'][i]['score'] == 21:
                JDict['joueurs'][i]['blackjack'] = True
                JDict['joueurs'][i]['ingame'] = False


        elif JDict['joueurs'][i]['ingame'] and JDict['joueurs'][i]['type']:

            print("\nJoueur :", JDict['joueurs'][i]['nom'])

            if JDict['joueurs'][i]['wallet'] <= 0:
                usrToDel.append(i)
            else:
                mise = floor(choixMise(JDict['joueurs'][i]['score'])*JDict['joueurs'][i]['wallet'])
                JDict['joueurs'][i]['wallet'] -= mise
                JDict['joueurs'][i]['mise'] += mise
                print(JDict['joueurs'][i]['nom'], "mise", mise, "OtterCoins")

            cartes2 = piocheCarte(JDict['pioche'], 2)
            print("Main du joueur : ", cartes2)
            for j in cartes2:
                JDict['joueurs'][i]['score'] += valeurCartes(j, JDict['joueurs'][i]['score'])
            print("Score actuel :", JDict['joueurs'][i]['score'])
            if JDict['joueurs'][i]['score'] == 21:
                JDict['joueurs'][i]['blackjack'] = True
                JDict['joueurs'][i]['ingame'] = False

    for i in usrToDel:
        del JDict['joueurs'][i]

    if JDict['croupier']['ingame']:

        cartes2 = piocheCarte(JDict['pioche'], 2)
        for j in cartes2:
            JDict['croupier']['score'] += valeurCartes(
                j, JDict['croupier']['score'])
        print("\nScore du croupier :", JDict['croupier']['score'])
        if JDict['croupier']['score'] == 21:
            JDict['croupier']['blackjack'] = True
            JDict['croupier']['ingame'] = False



def tourJoueur(j, JDict):

    if JDict['joueurs'][j]['ingame'] and not JDict['joueurs'][j]['type']:

        print("\nJoueur :", JDict['joueurs'][j]['nom'])
        print('Score partie: ', JDict['joueurs'][j]['score'])
        continueHuman(j, JDict)
        while JDict['joueurs'][j]['ingame']:
            carte = piocheCarte(JDict['pioche'])[0]
            val = valeurCartes(carte, JDict['joueurs'][j]['score'])
            print("Vous avez pioché : ", carte, "(valeur : "+str(val)+")")
            JDict['joueurs'][j]['score'] += val
            print("Votre score est donc de :", JDict['joueurs'][j]['score'])
            if JDict['joueurs'][j]['score'] == 21:
                JDict['joueurs'][j]['ingame'] = False
            elif JDict['joueurs'][j]['score'] > 21:
                print("Vous avez dépassé 21 ! Perdu !")
                JDict['joueurs'][j]['ingame'] = False
                JDict['joueurs'][j]['burst'] = True
            else:
                continueHuman(j, JDict)

    elif JDict['joueurs'][j]['ingame'] and JDict['joueurs'][j]['type']:
        print("\nJoueur :", JDict['joueurs'][j]['nom'])
        print('Score partie: ', JDict['joueurs'][j]['score'])
        continueIntel(j,JDict)
        while JDict['joueurs'][j]['ingame']:
            carte = piocheCarte(JDict['pioche'])[0]
            val = valeurCartes(carte, JDict['joueurs'][j]['score'])
            JDict['joueurs'][j]['score'] += val
            print("Nouveau score :", JDict['joueurs'][j]['score'])
            if JDict['joueurs'][j]['score'] == 21:
                JDict['joueurs'][j]['ingame'] = False
            elif JDict['joueurs'][j]['score'] > 21:
                print(JDict['joueurs'][j]['nom'], "a dépassé 21 ! Perdu !")
                JDict['joueurs'][j]['ingame'] = False
                JDict['joueurs'][j]['burst'] = True
            else:
                continueIntel(j,JDict)



def tourComplet(JDict):

    for j in JDict['joueurs']:
        tourJoueur(j,JDict)

    continueCroupier(JDict['croupier']['score'])
    while JDict['croupier']['ingame']:
        carte = piocheCarte(JDict['pioche'])[0]
        val = valeurCartes(carte, JDict['croupier']['score'])
        JDict['croupier']['score'] += val
        print("\nScore du croupier :", JDict['croupier']['score'])
        if JDict['croupier']['score'] == 21:
            JDict['croupier']['ingame'] = False
        elif JDict['croupier']['score'] > 21:
            print("Le croupier a dépassé !")
            JDict['croupier']['ingame'] = False
            JDict['croupier']['burst'] = True
        else:
            continueCroupier(JDict['croupier']['score'])



def partieComplete(JDict):
    tourComplet(JDict)

    print("\n\nPartie terminée")
    victorieux = gagnants(JDict)

    if len(victorieux) == 0:
        print("Il n'y a pas de gagnant, tout le monde a dépassé")

    elif victorieux[0] == 'croupier':
        for i in JDict['joueurs']:
            JDict['croupier']['wallet'] += JDict['joueurs'][i]['mise']
        JDict['croupier']['wallet'] += JDict['croupier']['mise']
        JDict['victoires']['croupier'] += 1
        print("Gagnant : croupier avec un score de", victorieux[1])
    
    else:
        for i in JDict['joueurs']:
            JDict['joueurs'][victorieux[0]]['wallet'] += JDict['joueurs'][i]['mise']
        JDict['joueurs'][victorieux[0]]['wallet'] += JDict['croupier']['mise']
        JDict['victoires'][JDict['joueurs'][victorieux[0]]['nom']] += 1
        print("Gagnant :", JDict['joueurs'][victorieux[0]]['nom'], "avec un score de", victorieux[1])

    GDict['partieFinie'] = False



def voulezVousPartir(JDict):
    print()
    if len(JDict['joueurs']) <= 0:
        print("Il n'y a plus de joueurs en jeu, vous ne pouvez rejoueur.")
        return
    else:
        for j in JDict['joueurs']:
            if not JDict['joueurs'][j]['type']:
                strAff = j+", voulez vous partir ? (o/n) "
                rep = ''
                while rep != 'o' and rep != 'n':
                    rep = input(strAff)
                if rep == 'o':
                    del JDict['joueurs'][j]
