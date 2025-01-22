from typing import List, Tuple


# Class for probability calculation
class ProbabilityCalculator:
    @staticmethod
    def calculate_win_probabilities(dice: List[List[int]]) -> List[List[float]]:
        n = len(dice)
        probabilities = [[0.0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i != j:
                    wins = sum(1 for a in dice[i] for b in dice[j] if a > b)
                    total = len(dice[i]) * len(dice[j])
                    probabilities[i][j] = wins / total
        return probabilities
