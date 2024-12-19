
import random
from quixo import Quixo, QuixoError
"""Importation eds modules qui permettent d'utiliser la class QuixoIA"""
class QuixoIA(Quixo):
    """Class qui permet a l'ordinateur de jouer de facon autonome"""
    def lister_les_coups_possibles(self, plateau, cube):
        """
        Liste tous les coups possibles pour un joueur donné.

        :param plateau: Une instance de la classe Plateau représentant l'état actuel du jeu.
        :param cube: Un caractère ("X" ou "O") représentant le joueur actuel.
        :return: Une liste de dictionnaires contenant les informations des coups 
        possibles (origine et direction).
        :raises QuixoError: Si le cube est invalide ou si la partie est déjà terminée.
        """
        # Vérifie que le cube est valide ("X" ou "O")
        if cube not in ("X", "O"):
            raise QuixoError('Le cube doit être "X" ou "O".')

        # Vérifie si la partie est terminée
        if self.partie_terminée():
            raise QuixoError("La partie est déjà terminée.")

        # Initialisation de la liste des coups possibles
        coups_possibles = []

        # Parcourt toutes les cases du plateau
        for i in range(1, 6):  # Pour chaque colone
            for j in range(1, 6):  # Pour chaque ligne
                # Vérifie si la case appartient au joueur ou est vide
                if plateau[i, j] == cube or plateau[i, j] == ' ':
                    # Si la case se trouve sur les bords horizontaux (gauche/droite)
                    if i == 1 and j != 1:  # Première Colone
                        coups_possibles.append({"origine": [i, j], "direction": "droite"})
                        if j > 1:  # Déplacement vers le haut
                            coups_possibles.append({"origine": [i, j], "direction": "haut"})
                        if j < 5:  # Déplacement vers le bas
                            coups_possibles.append({"origine": [i, j], "direction": "bas"})
                    if i == 5 and j != 5:  # dernière Colone
                        coups_possibles.append({"origine": [i, j], "direction": "gauche"})
                        if j > 1:  # Déplacement vers le haut
                            coups_possibles.append({"origine": [i, j], "direction": "haut"})
                        if j < 5:  # Déplacement vers le bas
                            coups_possibles.append({"origine": [i, j], "direction": "bas"})
                    # Si la case se trouve sur les bords verticaux (haut/bas)
                    if j == 1 and i != 5:  # Première ligne
                        coups_possibles.append({"origine": [i, j], "direction": "bas"})
                        if i > 1:  # Déplacement vers la gauche
                            coups_possibles.append({"origine": [i, j], "direction": "gauche"})
                        if i < 5:  # Déplacement vers la droite
                            coups_possibles.append({"origine": [i, j], "direction": "droite"})
                    if j == 5 and i != 1:  # dernière ligne
                        coups_possibles.append({"origine": [i, j], "direction": "haut"})
                        if i > 1:  # Déplacement vers la gauche
                            coups_possibles.append({"origine": [i, j], "direction": "gauche"})
                        if i < 5:  # Déplacement vers la droite
                            coups_possibles.append({"origine": [i, j], "direction": "droite"})

        # Retourne la liste complète des coups possibles
        return coups_possibles

    def analyser_le_plateau(self, plateau):
        """
        Analyse le plateau pour évaluer les lignes formées par les cubes de chaque joueur.

        :param plateau: Une instance de la classe Plateau représentant l'état actuel du jeu.
        :return: Un dictionnaire avec les clés "X" et "O", contenant des informations sur 
        les lignes formées.
        """
        analyse = {
            "X": {2: 0, 3: 0, 4: 0, 5: 0},
            "O": {2: 0, 3: 0, 4: 0, 5: 0}
        }

        for joueur in ("X", "O"):
            for longueur in range(2, 6):
                analyse[joueur][longueur] = plateau.compter_lignes(joueur, longueur)

        return analyse

    def partie_terminée(self):
        """
        Vérifie si la partie est terminée et identifie le vainqueur éventuel.

        :return: "X", "O" si un joueur a gagné, ou None si la partie n'est pas encore terminée.
        """
        # Vérification pour le joueur "X"
        if self.plateau.compter_lignes("X", 5) > 0:
            return "X"

        # Vérification pour le joueur "O"
        if self.plateau.compter_lignes("O", 5) > 0:
            return "O"

        # Si aucune ligne, colonne ou diagonale de 5 cubes n'est trouvée
        return None

    def trouver_un_coup_vainqueur(self, joueur):
        """
        Identifie un coup permettant de gagner la partie pour un joueur donné.

        :param joueur: Le symbole du joueur ("X" ou "O").
        :return: Un tuple ([x, y], direction) représentant le coup vainqueur ou None si 
        aucun coup n'est trouvé.
        """
        # Liste des coups possibles (obtenue via la méthode lister_les_coups_possibles)
        coups_possibles = self.lister_les_coups_possibles(self.plateau, joueur)

        # Parcours des coups possibles
        for coup in coups_possibles:
            # Simulation du coup : déplace le jeton et retourne une copie du tableau
            # avec la simulation
            plateau_simulé = self.plateau.simuler_coup(joueur, coup['origine'], coup['direction'])

            # Vérifie si la simulation cela entraîne une victoire
            if plateau_simulé.partie_terminée() == joueur:
                # Si c'est un coup gagnant, retourne le coup (coordonnée et direction)
                return coup

        # Si aucun coup gagnant n'est trouvé, retourne None
        return None

    def trouver_un_coup_bloquant(self, joueur):
        """
        Identifie un coup permettant de bloquer une victoire imminente de l'adversaire.

        :param joueur: Le symbole du joueur ("X" ou "O").
        :return: Un tuple ([x, y], direction) représentant le coup bloquant ou 
        None si aucun coup bloquant n'est trouvé.
        """
        # Identifier l'adversaire
        adversaire = "O" if joueur == "X" else "X"

        # Utiliser trouver_un_coup_vainqueur pour trouver si l'adversaire a un coup gagnant
        coup_gagnant_adversaire = self.trouver_un_coup_vainqueur(adversaire)

        # Si un tel coup existe
        if coup_gagnant_adversaire:
            # Et que ce coup est parmis la liste des coups possibles du joueurs,
            # retourne ce coup comme coup bloquant
            if coup_gagnant_adversaire in self.lister_les_coups_possibles(self.plateau, joueur):
                return coup_gagnant_adversaire

        # Aucun coup bloquant trouvé
        return None

    def jouer_un_coup(self, joueur):
        """
        Effectue un coup pour le joueur donné, en cherchant d'abord les coups gagnants ou bloquants.

        :param joueur: Le symbole du joueur ("X" ou "O").
        :return: Un tuple ([x, y], direction) représentant le coup joué.
        :raises QuixoError: Si la partie est terminée ou si le symbole du joueur est invalide.
        """
        if joueur not in ("X", "O"):
            raise QuixoError('Le symbole doit être "X" ou "O".')
        if self.partie_terminée():
            raise QuixoError("La partie est déjà terminée.")

        # Priorité 1 : Coup gagnant
        coup_vainqueur = self.trouver_un_coup_vainqueur(joueur)
        if coup_vainqueur:
            self.plateau.insérer_un_cube(joueur, coup_vainqueur['origine']
                                         , coup_vainqueur['direction'])
            return coup_vainqueur

        # Priorité 2 : Coup bloquant
        coup_bloquant = self.trouver_un_coup_bloquant(joueur)
        if coup_bloquant:
            self.plateau.insérer_un_cube(joueur, coup_bloquant['origine'],
                                          coup_bloquant['direction'])
            return coup_bloquant

        # Priorité 3 : Coup aléatoire si aucun autre choix
        coups_possibles = self.lister_les_coups_possibles(self.plateau, joueur)
        coup = random.choice(coups_possibles)
        self.plateau.insérer_un_cube(joueur, coup['origine'], coup['direction'])
        return coup
