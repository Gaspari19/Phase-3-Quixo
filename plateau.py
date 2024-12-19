"""Module Plateau

Classes:
    * Plateau - Classe principale du plateau de jeu Quixo.
"""

from copy import deepcopy

from quixo_error import QuixoError


class Plateau:
    """Classe plateau servant à générer un plateau de jeu, à acceder
      aux élément du plateau et à modifier leurs positions."""

    def __init__(self, plateau=None):
        """Constructeur de la classe Plateau

        Vous ne devez rien modifier dans cette méthode.

        Args:
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.plateau = self.générer_le_plateau(deepcopy(plateau))

    def état_plateau(self):
        """Retourne une copie du plateau

        Retourne une copie du plateau pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            list[list[str]]: La représentation du plateau
            tel que retourné par le serveur de jeu.
        """
        return deepcopy(self.plateau)

    def __str__(self):
        """Retourne une représentation en chaîne de caractères du plateau

        Déplacer le code de votre fonction formater_plateau ici et ajuster le en conséquence.

        Returns:
            str: Une représentation en chaîne de caractères du plateau.
        """
        lignes = ["   -------------------"]
        for i, ligne in enumerate(self.plateau):
            # Construire chaque ligne du plateau
            ligne_str = f"{i + 1} | " + " | ".join(ligne) + " |"
            lignes.append(ligne_str)
            # Ajouter une ligne de séparation si ce n'est pas la dernière ligne
            if i < 4:
                lignes.append("  |---|---|---|---|---|")

        # Ajouter la dernière ligne pour les indices des colonnes
        lignes.append("--|---|---|---|---|---|")
        lignes.append("  | 1   2   3   4   5 |")

        # Joindre toutes les lignes avec des sauts de ligne
        return "\n".join(lignes) + "\n"


    def __getitem__(self, position):
        """Retourne la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le plateau.

        Returns:
            str: La valeur à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
        """
        x, y = position

        if not 1 <= x <= 5 or not 1 <= y <= 5:
            raise QuixoError ("Les positions x et y doivent être entre 1 et 5 inclusivement")

        return self.plateau[y-1][x-1]

    def __setitem__(self, position, valeur):
        """Modifie la valeur à la position donnée

        Args:
            position (tuple[int, int]): La position (x, y) du cube sur le plateau.
            value (str): La valeur à insérer à la position donnée, soit "X", "O" ou " ".

        Raises:
            QuixoError: Les positions x et y doivent être entre 1 et 5 inclusivement.
            QuixoError: Valeur du cube invalide.
        """
        x, y = position

        if not 1 <= x <= 5 or not 1 <= y <= 5:
            raise QuixoError ("Les positions x et y doivent être entre 1 et 5 inclusivement")

        valeur_valides = {" ", "O", "X"}
        if valeur not in valeur_valides:
            raise QuixoError("Valeur du cube invalide.")

        self.plateau[y-1][x-1] = valeur

    def générer_le_plateau(self, plateau):
        """Génère un plateau de jeu

        Si un plateau est fourni, il est retourné tel quel.
        Sinon, si la valeur est None, un plateau vide de 5x5 est retourné.

        Args:
            plateau (list[list[str]] | None): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None.

        Returns:
            list[list[str]]: La représentation du plateau
                tel que retourné par le serveur de jeu.

        Raises:
            QuixoError: Format du plateau invalide.
            QuixoError: Valeur du cube invalide.
        """
        # Si le plateau est None, on crée un plateau 5x5 vide
        if plateau is None:
            return [[" " for _ in range(5)] for _ in range(5)]

        # Vérifier la dimension du plateau
        if len(plateau) != 5:
            raise QuixoError("Format du plateau invalide.")

        for ligne in plateau:
            if len(ligne) != 5:
                raise QuixoError("Format du plateau invalide.")

        # Vérifier que chaque case contient une valeur valide (" ", "X", "O")
        valeurs_valides = {" ", "X", "O"}
        for ligne in plateau:
            for cube in ligne:
                if cube not in valeurs_valides:
                    raise QuixoError("Valeur du cube invalide.")

        # Si tout est valide, on retourne le plateau fourni
        return plateau

    def insérer_un_cube(self, cube, origine, direction):
        """Insère un cube dans le plateau

        Cette méthode appelle la méthode d'insertion appropriée selon la direction donnée.

        À noter que la validation des positions sont faites dans
        les méthodes __setitem__ et __getitem__. Vous devez donc en faire usage dans
        les diverses méthodes d'insertion pour vous assurez que les positions sont valides.

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.
            direction (str): La direction de l'insertion, soit "haut", "bas", "gauche" ou "droite".

        Raises:
            QuixoError: La direction doit être "haut", "bas", "gauche" ou "droite".
            QuixoError: Le cube à insérer ne peut pas être vide.
        """
        # Valider le cube
        if cube not in {"X", "O", " "}:
            raise QuixoError("Le cube à insérer ne peut être que 'X' ou 'O'.")
        if cube == ' ':
            raise QuixoError("Le cube à insérer ne peut pas être vide.")

        # Valider la direction
        if direction not in {"haut", "bas", "gauche", "droite"}:
            raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")

        # Appeler la méthode d'insertion appropriée
        if direction == "bas":
            self.insérer_par_le_bas(cube, origine)
        elif direction == "haut":
            self.insérer_par_le_haut(cube, origine)
        elif direction == "gauche":
            self.insérer_par_la_gauche(cube, origine)
        elif direction == "droite":
            self.insérer_par_la_droite(cube, origine)

    def insérer_par_le_bas(self, cube, origine):
        """
        Insère un cube dans le plateau en direction du bas.

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.

        Raises:
            QuixoError: Si l'insertion par le bas est interdite.
        """
        x, y = origine

        # Validation
        if y == 5:
            raise QuixoError("Le cube ne peut pas être inséré dans cette direction.")

        # Déplacement des cubes
        for i in range(y, 5):
            self[x, i] = self[x, i + 1]

        self[x, 5] = cube

    def insérer_par_le_haut(self, cube, origine):
        """
        Insère un cube dans le plateau en direction du haut.

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.

        Raises:
            QuixoError: Si l'insertion par le haut est interdite.
        """
        x, y = origine

        # Validation
        if y == 1:
            raise QuixoError("Le cube ne peut pas être inséré dans cette direction.")

        # Déplacement des cubes
        for i in range(y, 1, -1):
            self[x, i] = self[x, i - 1]

        self[x, 1] = cube

    def insérer_par_la_gauche(self, cube, origine):
        """
        Insère un cube dans le plateau en direction de la gauche.

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.

        Raises:
            QuixoError: Si l'insertion par la gauche est interdite.
        """
        colone_origine, ligne_origine = origine

        # Validation
        if colone_origine == 1:
            raise QuixoError("Le cube ne peut pas être inséré dans cette direction.")

        # Déplacement des cubes
        for i in range(colone_origine, 1, -1):
            self[i, ligne_origine] = self[i - 1, ligne_origine]

        self[1, ligne_origine] = cube

    def insérer_par_la_droite(self, cube, origine):
        """
        Insère un cube dans le plateau en direction de la droite.

        Args:
            cube (str): La valeur du cube à insérer, soit "X" ou "O".
            origine (list[int]): La position [x, y] d'origine du cube à insérer.

        Raises:
            QuixoError: Si l'insertion par la droite est interdite.
        """
        colone_origine, ligne_origine = origine

        # Validation
        if colone_origine == 5:
            raise QuixoError("Le cube ne peut pas être inséré dans cette direction.")

        # Déplacement des cubes
        for i in range(colone_origine, 5):
            self[i, ligne_origine] = self[i + 1, ligne_origine]

        self[5, ligne_origine] = cube

    def compter_lignes(self, joueur, longueur):
        """
        Compte le nombre de groupes de cubes d'une certaine longueur appartenant à un joueur donné 
        sur une ligne, une colonne ou une diagonale.

        :param joueur: "X" ou "O" pour identifier le joueur.
        :param longueur: Longueur des groupes à analyser (2, 3, 4, ou 5).
        :return: Nombre total de groupes trouvés.
        """
        total_groupes = 0

        # Vérification des lignes
        for ligne in range(1, 6):
            contenu = [self[col, ligne] for col in range(1, 6)]
            if contenu.count(joueur) == longueur:
                total_groupes += 1

        # Vérification des colonnes
        for col in range(1, 6):
            contenu = [self[col, ligne] for ligne in range(1, 6)]
            if contenu.count(joueur) == longueur:
                total_groupes += 1

        # Vérification des diagonales
        diagonale_principale = [self[i, i] for i in range(1, 6)]
        diagonale_secondaire = [self[i, 6 - i] for i in range(1, 6)]

        if diagonale_principale.count(joueur) == longueur:
            total_groupes += 1
        if diagonale_secondaire.count(joueur) == longueur:
            total_groupes += 1

        return total_groupes

    def simuler_coup(self,cube,origine, direction):
        """
        Simule un coup en déplaçant un cube depuis une position donnée dans une direction donnée.
        
        :param x: Colonne d'origine du cube (1 à 5).
        :param y: Ligne d'origine du cube (1 à 5).
        :param direction: Direction du déplacement ("haut", "bas", "gauche", "droite").
        :param joueur: Le joueur effectuant le coup ("X" ou "O").
        :return: Une nouvelle instance de Plateau représentant l'état simulé du 
        plateau après le coup.
        :raises QuixoError: Si les paramètres du coup sont invalides.
        """
        # Crée une copie du plateau actuel pour la simulation
        plateau_simule  =  Plateau(self.état_plateau())

        # Déplace le cube sur le plateau simulé
        plateau_simule.insérer_un_cube(cube,origine, direction)

        # Retourne le plateau simulé
        return plateau_simule

    def partie_terminée(self):
        """
        Vérifie si la partie est terminée et identifie le vainqueur éventuel.

        :return: "X", "O" si un joueur a gagné, ou None si la partie n'est pas encore terminée.
        """
        # Vérification pour le joueur "X"
        if self.compter_lignes("X", 5) > 0:
            return "X"

        # Vérification pour le joueur "O"
        if self.compter_lignes("O", 5) > 0:
            return "O"

        # Si aucune ligne, colonne ou diagonale de 5 cubes n'est trouvée
        return None
