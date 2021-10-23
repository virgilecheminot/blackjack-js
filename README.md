<div align="center">
 <h1>
    Projet INF101 : Le jeu de Blackjack
  </h1>
  <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">
    <img alt="Licence Creative Commons" style="border-width:0;" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" />
  </a> <br />
  Ce projet est mis à disposition selon les termes de la <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">
    Licence Creative Commons Attribution - Pas d&#39;Utilisation Commerciale - Pas de Modification 4.0 International
  </a>.
</div>

#
## Règles du jeu :
On s’intéresse à une version simplifiée du jeu de Blackjack, qui se joue avec plusieurs paquets de 52 cartes. Chaque paquetde 52 cartes est divisé en 4 couleurs (pique, cœur, trèfle, carreau), avec 13 cartes par couleur, numérotées de 1 (as) à 10, puis valet, dame, roi.

Le but d’une partie de Blackjack est de s’approcher le plus possible de 21 points, sans dépasser ce total. Les valeurs numériques des cartes sont les suivantes :

- Les cartes numérotées de 2 à 10 valent autant de points que leur numéro (donc entre 2 et 10 points)
- L’as vaut soit 1 soit 11 points, au choix du joueur
- Les figures (valet, dame, roi) valent chacune 10 points

Les joueurs commencent la partie avec 2 cartes. A son tour chaque joueur peut choisir de s’arrêter avec son totalactuel, ou de piocher une nouvelle carte (face cachée) pour l’ajouter à son total. Si le nouveau total dépasse alors 21 points, il perd immédiatement. Si le total égale 21 points exactement, il gagne immédiatement. Dans les autres cas, ilreste en jeu et pourra à son prochain tour à nouveau choisir de continuer ou s’arrêter. Quand plus aucun joueur n’est en jeu (tous ont arrêté ou perdu) alors le gagnant est le joueur le plus proche de 21. Remarque : une version plus comptète des règles du Blackjack se trouve ici : https://www.guide-blackjack.com/Regles-du-black-jack.html