## PAQUET DE CARTES ##

from math import *
from random import *
from numpy import random as nprd


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


def valeurAs(score):
    if score+11 <= 21:
        return 11
    else:
        return 1


def initPioche(n):
    pioche = []
    cartes = paquet()
    for i in range(n):
        pioche.extend(cartes)
    shuffle(pioche)
    return pioche


def valeurCartes(carte, score):
    carte_WO_couleur = carte.split()[0]
    if carte_WO_couleur == 'as':
        return valeurAs(score)
    else:
        return ValCartes[carte_WO_couleur]


def piocheCarte(p, x=1):
    piochees = []
    for i in range(x):
        piochees.append(p.pop(0))
    return piochees

# JOUEURS ET SCORES


def initJoueurs(JDict,n):
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


def initScores(JDict, valeur, v=0):
    for i in JDict['joueurs']:
        JDict['joueurs'][i][valeur] = v
    JDict['croupier'][valeur] = v

def initVictoires(JDict):
    for i in JDict['joueurs']:
        JDict['victoires'][JDict['joueurs'][i]['nom']] = 0



def premierTour(GDict,JDict):
    print("\n\nPremier tour:")
    for i in JDict['joueurs']:

        if JDict['joueurs'][i]['ingame'] and not JDict['joueurs'][i]['type']:

            print("\nJoueur :", JDict['joueurs'][i]['nom'])
            cartes2 = piocheCarte(GDict['pioche'], 2)
            print("Main du joueur : ", cartes2)
            for j in cartes2:
                JDict['joueurs'][i]['score'] += valeurCartes(j,JDict['joueurs'][i]['score'])
            print("Score actuel :", JDict['joueurs'][i]['score'])
            if JDict['joueurs'][i]['score'] == 21:
                GDict['partieFinie'] = True
            if JDict['joueurs'][i]['wallet'] <= 0:
                print("Vous n'avez plus d'OtterCoins, vous ne pouvez plus jouer")
                del JDict['joueurs'][i]
            else:
                print(f"Combien voulez-vous miser ? ({JDict['joueurs'][i]['wallet']} OtterCoins restants) : ", end='')
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


        elif JDict['joueurs'][i]['ingame'] and JDict['joueurs'][i]['type']:

            print("\nJoueur :", JDict['joueurs'][i]['nom'])
            cartes2 = piocheCarte(GDict['pioche'], 2)
            print("Main du joueur : ", cartes2)
            for j in cartes2:
                JDict['joueurs'][i]['score'] += valeurCartes(j,JDict['joueurs'][i]['score'])
            print("Score actuel :", JDict['joueurs'][i]['score'])
            if JDict['joueurs'][i]['score'] == 21:
                GDict['partieFinie'] = True
            if JDict['joueurs'][i]['wallet'] <= 0:
                del JDict['joueurs'][i]
            else:
                mise = floor(choixMise(JDict['joueurs'][i]['score'])*JDict['joueurs'][i]['wallet'])
                JDict['joueurs'][i]['wallet'] -= mise
                JDict['joueurs'][i]['mise'] += mise
                print(JDict['joueurs'][i]['nom'], "mise", mise, "OtterCoins")
    if JDict['croupier']['ingame']:
        cartes2 = piocheCarte(GDict['pioche'], 2)
        for j in cartes2:
            JDict['croupier']['score'] += valeurCartes(j,JDict['croupier']['score'])
        print("\nScore du croupier :", JDict['croupier']['score'])
        if JDict['croupier']['score'] == 21:
            GDict['partieFinie'] = True
        mise = floor(choixMise(JDict['croupier']['score'])*JDict['croupier']['wallet'])
        JDict['croupier']['wallet'] -= mise
        JDict['croupier']['mise'] += mise
        print("Le croupier mise", JDict['croupier']['mise'],"OtterCoins")



def choixMise(score):
    if score <= 10:
        p = score/10
    elif score < 21:
        p = 1-((score-11)/10)
    elif score == 21:
        p = 1
    return p


def gagnant(scores):
    scoreMax = 0
    gagnant = ''
    for i in scores:
        if scores[i] == 21:
            return i
        if 21 > scores[i] > scoreMax:
            gagnant = i
            scoreMax = scores[i]
    return gagnant


def continueHuman():
    c = ''
    while c != 'oui' and c != 'non':
        c = str(input('Piocher ? (oui / non) : '))
    if c == 'oui':
        return True
    else:
        return False

def continueAlea():
    return choice([False,True])

def continuePara(p=0.5):
    return nprd.choice([False,True],p=[1-p,p])

def continueIntel(j,scores):
    if scores[j] <= 10:
        p = 1
    elif scores[j] < 21:
        p = 1-((scores[j]-11)/10)
    else:
        p = 0
    return continuePara(p)

def continueClassic(j,scores):
    if scores[j] < 17:
        return True
    else:
        return False


def tourJoueur(j, GDict, JDict):
    print("\n\nTour numéro :", GDict['nbtour']+1)
    if j != 'croupier':
        print("\nJoueur :", j)
        print('score partie: ', JDict['scores'][j])
        replay = continueHuman()
        if replay:
            carte = piocheCarte(GDict['pioche'])[0]
            val = valeurCartes(carte, JDict['scores'], j)
            print("Vous avez pioché : ", carte, "(valeur : "+str(val)+")")
            JDict['scores'][j] += val
            print("Votre score est donc de :", JDict['scores'][j])
            if JDict['scores'][j] == 21:
                JDict['ingame'].clear()
                return
            elif JDict['scores'][j] > 21:
                print("Vous avez dépassé 21 ! Perdu !")
                JDict['ingame'].remove(j)
                del JDict['scores'][j]
                return
        elif not replay:
            JDict['ingame'].remove(j)
            return
    else:
         replay = continueIntel(j,JDict['scores'])
         if replay:
            carte = piocheCarte(GDict['pioche'])[0]
            val = valeurCartes(carte, JDict['scores'], j)
            JDict['scores'][j] += val
            print("\nScore du croupier :",JDict['scores'][j])
            if JDict['scores'][j] == 21:
                JDict['ingame'].clear()
                return
            elif JDict['scores'][j] > 21:
                print("Le croupier a dépassé !")
                JDict['ingame'].remove(j)
                del JDict['scores'][j]
                return
         elif not replay:
            print("\nLe croupier ne pioche pas")
            JDict['ingame'].remove(j)
            return


def tourComplet(GDict,JDict):
    for i in JDict['ingame']:
        tourJoueur(i, GDict,JDict)
        if partieFinie(JDict['ingame']):
            break


def partieFinie(joueurs):
    if len(joueurs) == 0:
        return True
    else:
        return False


def partieComplete(GDict,JDict):
    while not partieFinie(JDict['ingame']):
        tourComplet(GDict,JDict)
        GDict['nbtour'] += 1
    print("\n\nPartie terminée")
    victorieux = gagnant(JDict['scores'])
    for i in JDict['mises']:
        JDict['wallet'][victorieux] += JDict['mises'][i]
    print("Gagnant :", victorieux)
    JDict['victoires'][victorieux] += 1


def voulezVousPartir(JDict):
    print()
    usrToDel = []
    for j in JDict['listeJ']:
        if j != 'croupier':
            strAff = j+", voulez vous partir ? (o/n) "
            rep = ''
            while rep != 'o' and rep != 'n':
                rep = input(strAff)
            if rep == 'o':
                usrToDel.append(j)
    for i in usrToDel:
        JDict['listeJ'].remove(i)
        del JDict['wallet'][i]
