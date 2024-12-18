"""Tests Quixo

Ce module contient des tests unitaires pour le projet Quixo.
"""

from plateau import Plateau
from quixo import Quixo


def test_formater_le_damier_pour_une_nouvelle_partie():
    """Test de la fonction formater_le_damier"""
    plateau = Plateau()

    attendu = (
        "   -------------------\n"
        "1 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "2 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "3 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "4 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "5 |   |   |   |   |   |\n"
        "--|---|---|---|---|---|\n"
        "  | 1   2   3   4   5 |\n"
    )

    résultat = str(plateau)

    assert résultat == attendu, "Échec du test de formater damier pour une nouvelle partie"


def test_formater_le_jeu_pour_une_nouvelle_partie():
    """Test de la fonction formater_le_jeu_nouvelle_partie"""
    joueurs = ["josmi42", "automate"]

    quixo = Quixo(joueurs)

    attendu = (
        "Légende:\n"
        "   X=josmi42\n"
        "   O=automate\n"
        "   -------------------\n"
        "1 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "2 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "3 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "4 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "5 |   |   |   |   |   |\n"
        "--|---|---|---|---|---|\n"
        "  | 1   2   3   4   5 |\n"
    )

    résultat = str(quixo)

    assert résultat == attendu, "Échec du test de formater le jeu pour une nouvelle partie"


def test_formater_le_jeu_pour_une_partie_avancée():
    """Test de la fonction formater_le_jeu(avancé)"""
    joueurs = ["josmi42", "automate"]
    plateau = [
        [" ", " ", "X", " ", " "],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", "O"],
        [" ", " ", " ", " ", " "],
        [" ", " ", " ", " ", " "],
    ]

    quixo = Quixo(joueurs, plateau)

    attendu = (
        "Légende:\n"
        "   X=josmi42\n"
        "   O=automate\n"
        "   -------------------\n"
        "1 |   |   | X |   |   |\n"
        "  |---|---|---|---|---|\n"
        "2 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "3 |   |   |   |   | O |\n"
        "  |---|---|---|---|---|\n"
        "4 |   |   |   |   |   |\n"
        "  |---|---|---|---|---|\n"
        "5 |   |   |   |   |   |\n"
        "--|---|---|---|---|---|\n"
        "  | 1   2   3   4   5 |\n"
    )

    résultat = str(quixo)

    assert résultat == attendu, "Échec du test de formater le jeu pour une partie avancée"


if __name__ == "__main__":
    test_formater_le_damier_pour_une_nouvelle_partie()
    print("Test de formater le damier pour une nouvelle partie réussi")
    test_formater_le_jeu_pour_une_nouvelle_partie()
    print("Test de formater le jeu pour une nouvelle partie réussi")
    test_formater_le_jeu_pour_une_partie_avancée()
    print("Test de formater le jeu pour une partie avancée réussi")
