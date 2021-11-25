from blackjack import *

nbjoueurs = int(input('Nombre de joueurs : '))
joueurs = initJoueurs(nbjoueurs)
scores = initScores(joueurs)
victoires = initVictoires(joueurs)
pioche = initPioche(nbjoueurs)

rejouer = True
while rejouer:
    nbtour = 0
    joueursEnCours = joueurs
    partieComplete(joueursEnCours,nbtour,scores,pioche,victoires)
    if input("Voulez vous lancer une nouvelle partie ? (o/n)") == 'o':
        rejouer = True
    else :
        rejouer = False
print("Vous avez terminé, le programme va maintenant se fermer.")