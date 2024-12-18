"""Module Quixo

Classes:
    * Quixo - Classe principale du jeu Quixo.
    * QuixoError - Classe d'erreur pour le jeu Quixo.

Functions:
    * interpréter_la_commande - Génère un interpréteur de commande.
"""

import argparse

from quixo_error import QuixoError

from plateau import Plateau


class Quixo:
    """Class principale qui gère le jeu"""
    def __init__(self, joueurs, plateau=None) -> None:
        """Constructeur de la classe Quixo

        Vous ne devez rien modifier dans cette méthode.

        Args:
            joueurs (list[str]): La liste des deux joueurs.
                Le premier joueur possède le symbole "X" et le deuxième "O".
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.joueurs = joueurs
        self.plateau = Plateau(plateau)

    def état_partie(self):
        """Retourne une copie du jeu

        Retourne une copie du jeu pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            dict: La représentation du jeu tel que retourné par le serveur de jeu.
        """
        return {
            "joueurs": self.joueurs,
            "plateau": self.plateau.état_plateau(),
        }

    def __str__(self):
        """Retourne une représentation en chaîne de caractères de la partie

        Déplacer le code de vos fonctions formater_légende et formater_jeu ici.
        Adaptez votre code en conséquence et faites appel à Plateau
        pour obtenir la représentation du plateau.

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        legende = f"Légende:\n   X={self.joueurs[0]}\n   O={self.joueurs[1]}\n"

        return legende + str(self.plateau)

    def déplacer_un_cube(self, joueur, origine, direction):
        """déplacer_un_cube dans une direction donnée.

        Applique le changement au Plateau de jeu

        Args:
            pion (str): Le pion à déplacer, soit "X" ou "O".
            origine (list[int]): La position (x, y) du pion sur le plateau.
            direction (str): La direction du déplacement, soit "haut", "bas", "gauche" ou "droite".
        """
        if joueur == self.joueurs[1]:
            cube = "X"
        else:
            cube = "O"
        # Appeler la méthode insérer_un_cube sur le plateau
        self.plateau.insérer_un_cube(cube, origine, direction)

    def choisir_un_coup(self):
        """Demander le prochain coup à jouer au joueur.

        Déplacer le code de votre fonction récupérer_le_coup ici et ajuster le en conséquence.
        Vous devez maintenant valider les entrées de l'utilisateur.

        Returns:
            tuple: Tuple de 2 éléments composé de l'origine du bloc à déplacer et de sa direction.
                L'origine est une liste de 2 entiers [x, y].
                La direction est une chaîne de caractères.

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
            QuixoError: La direction doit être "haut", "bas", "gauche" ou "droite".

        Examples:
            Donnez la position d'origine du bloc (x,y) :
            Quelle direction voulez-vous insérer? ('haut', 'bas', 'gauche', 'droite') :
        """
        origine_ch = input("Donnez la position d'origine du cube (x,y) : ")

        try:
            origine_list = origine_ch.split(",")
            origine = [int(elt) for elt in origine_list]
            if not 1 <= origine[0] <= 5 or not 1 <= origine[1] <= 5:
                raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")
        except ValueError as _:
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.") from _

        vers = input("Quelle direction voulez-vous insérer? ('haut', 'bas', 'gauche', 'droite') : ")

        if vers not in {'haut', 'bas', 'gauche', 'droite'}:
            raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")

        return origine, vers


def interpréter_la_commande():
    """Génère un interpréteur de commande.
    Returns:
        Namespace: Un objet Namespace tel que retourné par parser.parse_args().
            Cet objet aura l'attribut «idul» représentant l'idul du joueur
            et l'attribut «parties» qui est un booléen True/False.
    """
    parser = argparse.ArgumentParser(description="Quixo")

    parser.add_argument("idul",type=str,help="IDUL du joueur")

    return parser.parse_args()
