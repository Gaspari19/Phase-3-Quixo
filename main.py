"""
Jeu Quixo 

Ce programme permet de jouer au jeu Quixo.
"""

from api import initialiser_partie, jouer_un_coup, récupérer_une_partie
from quixo import Quixo, interpréter_la_commande
from quixo_ia import QuixoIA
from plateau import Plateau

SECRET = "e7cd4ac8-6447-4447-8019-e26b53e90ae9"

if __name__ == "__main__":
    # Analyse des arguments de la ligne de commande
    args = interpréter_la_commande()

    # Initialisation de la partie
    id_partie, joueurs, plateau = initialiser_partie(args.idul, SECRET)

    if args.autonome:
        print("Mode autonome activé : L'IA jouera contre le serveur.")
        # Créer une instance de l'IA
        ia = QuixoIA(joueurs, plateau)

        while True:
            # Affiche l'état actuel de la partie
            print("\nÉtat du plateau :")
            print(ia)

            # L'IA réfléchit et choisit son coup
            print("\nL'IA réfléchit à son coup...")
            try:
                coup = ia.jouer_un_coup('X')  # IA joue avec le symbole 'X'
                print(f"IA joue : {coup}")

                # Envoyer le coup au serveur
                id_partie, joueurs, plateau = jouer_un_coup(
                    id_partie,
                    coup['origine'],  # Origine du cube
                    coup['direction'],  # Direction d'insertion
                    args.idul,
                    SECRET
                )

                # Mise à jour du plateau pour l'IA
                ia.plateau = Plateau(plateau)

                # Vérifie si la partie est terminée
                id_partie, joueurs, plateau, vainqueur = récupérer_une_partie(id_partie,
                                                             args.idul, SECRET)
                if vainqueur:
                    print(f"\nPartie terminée ! Le gagnant est : {vainqueur}")
                    break
            except Exception as e:
                print(f"Erreur pendant le coup de l'IA : {e}")
                break
    else:
        print("Mode interactif activé : Joueur humain contre le serveur.")
        while True:
            # Créer une instance de Quixo
            quixo = Quixo(joueurs, plateau)

            # Affiche l'état du plateau
            print("\nÉtat du plateau :")
            print(quixo)

            # Demande au joueur de choisir son prochain coup
            try:
                origine, direction = quixo.choisir_un_coup()

                # Envoyer le coup au serveur
                id_partie, joueurs, plateau = jouer_un_coup(
                    id_partie,
                    origine,
                    direction,
                    args.idul,
                    SECRET
                )

                # Vérifie si la partie est terminée
                id_partie, joueurs, plateau, vainqueur = récupérer_une_partie(id_partie,
                                                                               args.idul, SECRET)
                if vainqueur:
                    print(f"\nPartie terminée ! Le gagnant est : {vainqueur}")
                    break
            except Exception as e:
                print(f"Erreur pendant le tour du joueur : {e}")
                break
