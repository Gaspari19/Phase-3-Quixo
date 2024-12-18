"""Creation du fichier quixo_error pour gérér les erreurs"""
class QuixoError(Exception):
    """Class qui gère les exceptions du jeu"""

    def __init__(self, message):
        """Module d'initialisation de la classe : c'est le meme
          que celle de sa classe mère"""
        super().__init__(message)
