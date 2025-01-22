from typing import List, Tuple


# Helper class for parsing dice configurations
class DiceParser:
    @staticmethod
    def parse(args: List[str]) -> List[List[int]]:
        dice = []
        for arg in args:
            try:
                dice_set = list(map(int, arg.split(",")))
                if len(dice_set) != 6:
                    raise ValueError("Each dice must have exactly 6 integers.")
                dice.append(dice_set)
            except ValueError:
                raise ValueError(
                    f"Invalid dice configuration: '{arg}'. Ensure it's 6 comma-separated integers."
                )
        if len(dice) < 3:
            raise ValueError("At least 3 dice configurations are required.")
        return dice
