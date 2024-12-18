from quixo import Quixo, QuixoError, Plateau

class QuixoIA(Quixo):

    def lister_les_coups_possibles(self, plateau, cube):
        """
        Liste tous les coups possibles pour un joueur donné.
        
        :param plateau: Une instance de la classe Plateau représentant l'état actuel du jeu.
        :param cube: Un caractère ("X" ou "O") représentant le joueur actuel.
        :return: Une liste de dictionnaires contenant les informations des coups possibles (origine et direction).
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
        :return: Un dictionnaire avec les clés "X" et "O", contenant des informations sur les lignes formées.
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
        if self.compter_lignes("X", 5) > 0:
            return "X"
        
        # Vérification pour le joueur "O"
        if self.compter_lignes("O", 5) > 0:
            return "O"
        
        # Si aucune ligne, colonne ou diagonale de 5 cubes n'est trouvée
        return None
    
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
            contenu = [self.plateau[(col, ligne)] for col in range(1, 6)]
            if contenu.count(joueur) == longueur:
                total_groupes += 1

        # Vérification des colonnes
        for col in range(1, 6):
            contenu = [self.plateau[(col, ligne)] for ligne in range(1, 6)]
            if contenu.count(joueur) == longueur:
                total_groupes += 1

        # Vérification des diagonales
        diagonale_principale = [self.plateau[(i, i)] for i in range(1, 6)]
        diagonale_secondaire = [self.plateau[(i, 6 - i)] for i in range(1, 6)]
        
        if diagonale_principale.count(joueur) == longueur:
            total_groupes += 1
        if diagonale_secondaire.count(joueur) == longueur:
            total_groupes += 1

        return total_groupes
    
    def trouver_un_coup_vainqueur(self, joueur):
        """
        Identifie un coup permettant de gagner la partie pour un joueur donné.

        :param joueur: Le symbole du joueur ("X" ou "O").
        :return: Un tuple ([x, y], direction) représentant le coup vainqueur ou None si aucun coup n'est trouvé.
        """
        coups_possibles = self.lister_les_coups_possibles(self.plateau, joueur)
        for coup in coups_possibles:
            i,j=coup['origine']
            direction = coup['direction']

    
IA= QuixoIA(['MOI','TOI'])
tableau = [
    ["O", " ", "X", " ", " "],
    [" ", "X", " ", "X", "O"],
    [" ", "O", "X", " ", "O"],
    [" ", "X", "X", "X", "O"],
    ["X", " ", " ", " ", "O"]
]
table=Plateau(tableau)
print(table,IA.lister_les_coups_possibles(table,'X'), IA.analyser_le_plateau(table))
