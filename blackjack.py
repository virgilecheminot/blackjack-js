## PAQUET DE CARTES ##

from random import *


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
    ]  # fantastique


ValCartes = {
    'as': [1, 11],
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


def valeurAs(scores, joueur):
    if scores[joueur]+11 <= 21:
        return 1
    else:
        return 0


def initPioche(n):
    pioche = []
    cartes = paquet()
    for i in range(n):
        shuffle(cartes)
        pioche.extend(cartes)
    return pioche


def valeurCartes(carte, scores, joueur):
    carte_WO_couleur = carte.split()[0]
    if carte_WO_couleur == 'as':
        return ValCartes['as'][valeurAs(scores, joueur)]
    else:
        return ValCartes[carte_WO_couleur]


def piocheCarte(p, x=1):
    piochees = []
    for i in range(x):
        piochees.append(p.pop(0))
    return piochees

# JOUEURS ET SCORES


def initJoueurs(n):
    nomsJoueurs = []
    for i in range(n):
        nomsJoueurs.append(input(f'Nom du joueur {i+1} : '))
    return nomsJoueurs


def initScores(joueurs, v=0):
    scores = {}
    for i in joueurs:
        scores[i] = v
    return scores


def premierTour(joueurs, scores, pioche,portefeuille,mises):
    for i in joueurs:
        print("Joueur :", i)
        cartes2 = piocheCarte(pioche, 2)
        print("Main du joueur : ",cartes2)
        for j in cartes2:
            scores[i] += valeurCartes(j, scores, i)
        print("Score actuel :", scores[i])
        if portefeuille[i] <= 0:
            print("Vous n'avez plus d'OtterCoins, vous ne pouvez plus jouer")
            joueurs.remove(i)
            del scores[i]
        else:
            print(f"Combien voulez-vous miser ? ({portefeuille[i]} OtterCoins restants) : ",end='')
            mise = 101
            while mise > portefeuille[i]:
                mise = int(input())
            portefeuille[i] -= mise
            mises[i] += mise

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


def continuer():
    c = ''
    while c != 'oui' and c != 'non':
        c = str(input('Continuer ? (oui / non) : '))
    if c == 'oui':
        return True
    else:
        return False


def tourJoueur(j, nbtour, scores, joueurs, pioche):
    print("\nTour numéro :", nbtour+1)
    print("Joueur :", j)
    print('score partie: ', scores[j])
    replay = continuer()
    if replay:
        carte = piocheCarte(pioche)[0]
        val = valeurCartes(carte, scores, j)
        print("Vous avez pioché : ", carte, "(valeur : "+str(val)+")")
        scores[j] += val
        print("Votre score est donc de :", scores[j])
        if scores[j] == 21:
            joueurs.clear()
            return
        elif scores[j] > 21:
            print("Vous avez dépassé 21 ! Perdu !")
            joueurs.remove(j)
            del scores[j]
            return
    elif not replay:
        joueurs.remove(j)
        return


def tourComplet(joueurs, nbtour, scores, pioche):
    for i in joueurs:
        tourJoueur(i, nbtour, scores, joueurs, pioche)
        if partieFinie(joueurs):
            break


def partieFinie(joueurs):
    if len(joueurs) == 0:
        return True
    else:
        return False


def partieComplete(joueurs, nbtour, scores, pioche, victoires, portefeuille, mises):
    while not partieFinie(joueurs):
        tourComplet(joueurs, nbtour, scores, pioche)
        nbtour += 1
    if partieFinie(joueurs):
        print("Partie terminée")
        victorieux = gagnant(scores)
        for i in mises:
            portefeuille[victorieux] += mises[i]
        print("Gagnant :", victorieux)
        victoires[victorieux] += 1

def voulezVousPartir(joueurs, portefeuille):
    usrToDel = []
    for j in joueurs:
        strAff = j+", voulez vous partir ? (o/n) "
        rep = input(strAff)
        if rep == 'o':
            usrToDel.append(j)
    for i in usrToDel:
        joueurs.remove(i)
        del portefeuille[i]