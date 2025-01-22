from tabulate import tabulate
from typing import List


class HelpMenu:
    @staticmethod
    def display_help(dice: List[List[int]], probabilities: List[List[float]]):
        headers = ["Dice"] + [f"Dice {i}" for i in range(len(dice))]
        table = [
            [f"Dice {i}"] + [f"{prob:.2f}" for prob in row]
            for i, row in enumerate(probabilities)
        ]
        print("\nDice Probabilities (P1 wins vs. P2):\n")
        print(tabulate(table, headers=headers, tablefmt="grid"))
