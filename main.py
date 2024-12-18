"""Jeu Quixo

Ce programme permet de joueur au jeu Quixo.
"""

from api import initialiser_partie, jouer_un_coup
from quixo import Quixo, interpréter_la_commande

# Mettre ici votre secret récupérer depuis le site de PAX
SECRET = "e7cd4ac8-6447-4447-8019-e26b53e90ae9"


if __name__ == "__main__":
    args = interpréter_la_commande()
    id_partie, joueurs, plateau = initialiser_partie(args.idul, SECRET)
    while True:
        # Créer une instance de Quixo
        quixo = Quixo(joueurs, plateau)
        # Afficher la partie
        print(quixo)
        # Demander au joueur de choisir son prochain coup
        origine, direction = quixo.choisir_un_coup()
        # Envoyez le coup au serveur
        id_partie, joueurs, plateau = jouer_un_coup(
            id_partie,
            origine,
            direction,
            args.idul,
            SECRET,
        )
