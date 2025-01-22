import sys
from typing import List
from helpFunc import HelpMenu
from probabilityCalc import ProbabilityCalculator


class Modulator:
    @staticmethod
    def module(computer_num: int, dice: List[List[int]]) -> int:
        valid_inputs = set(["0", "1", "2", "3", "4", "5"])
        user_num_input = (
            input(
                f"Add your number modulo 6.\n0 - 0\n1 - 1\n2 - 2\n3 - 3\n4 - 4\n5 - 5\nX - exit\n? - help\nYour selection: "
            )
            .strip()
            .lower()
        )
        while user_num_input not in valid_inputs:
            if user_num_input == "x":
                sys.exit("Game exited.")
            elif user_num_input == "?":
                probabilities = ProbabilityCalculator.calculate_win_probabilities(
                    [d.values for d in dice]
                )
                HelpMenu.display_help([d.values for d in dice], probabilities)
            else:
                print("Invalid selection.")

            user_num_input = input(
                f"Again add your number modulo 6.\n0 - 0\n1 - 1\n2 - 2\n3 - 3\n4 - 4\n5 - 5\nX - exit\n? - help\nYour selection: "
            )

        try:
            user_num = int(user_num_input)
            if 0 <= user_num <= 5:
                result = (computer_num + user_num) % 6
                return result, user_num
        except ValueError:
            pass
        print("Invalid selection.")
        sys.exit("Game exited.")
