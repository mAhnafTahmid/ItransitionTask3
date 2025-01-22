import sys
import random
from typing import List

from fairRandom import FairRandomProtocol
from helpFunc import HelpMenu
from inputValidation import DiceParser
from moduloCalc import Modulator
from probabilityCalc import ProbabilityCalculator


class Dice:
    def __init__(self, values: List[int]):
        self.values = values


class DiceGame:
    def __init__(self, dice: List[List[int]]):
        self.dice = [Dice(values) for values in dice]
        self.used_dice = set()

    def roll(self) -> int:
        return FairRandomProtocol.generate_and_prove(5)

    def get_dice_selection(self, exclude: int = -1) -> int:
        while True:
            print("Choose your dice:")
            for i, d in enumerate(self.dice):
                if i != exclude:
                    print(f"{i} - {d.values}")
            print("X - Exit\n? - Help")
            choice = input("Your selection: ").strip().lower()
            if choice == "x":
                sys.exit("Game exited.")
            elif choice == "?":
                probabilities = ProbabilityCalculator.calculate_win_probabilities(
                    [d.values for d in self.dice]
                )
                HelpMenu.display_help([d.values for d in self.dice], probabilities)
            else:
                try:
                    idx = int(choice)
                    if idx != exclude and 0 <= idx < len(self.dice):
                        return idx
                except ValueError:
                    pass
                print("Invalid selection. Try again.")

    def play(self):
        print("Let's determine who makes the first move.")
        computer_choice, hmac_value, key = FairRandomProtocol.generate_and_prove(1)
        print(f"I selected a random value in the range 0..1 \n(HMAC={hmac_value}).")

        user_guess = self.get_user_guess()
        user_guess = int(user_guess)
        print(f"My selection: {computer_choice}\n(KEY={key.hex()})")
        user_first = user_guess == computer_choice

        if user_first:
            print(f"You make the first move.")
            user_dice_idx = self.get_dice_selection()
            self.used_dice.add(user_dice_idx)
            computer_dice_idx = self.get_computer_dice_selection()
        else:
            computer_dice_idx = self.get_computer_dice_selection()
            self.used_dice.add(computer_dice_idx)
            computer_selected_dice = self.dice[computer_dice_idx].values
            print(
                f"I make the first move and choose the {computer_selected_dice} dice."
            )
            user_dice_idx = self.get_dice_selection(exclude=computer_dice_idx)

        print(f"You chose the {self.dice[user_dice_idx].values} dice.")
        if user_first:
            print(f"I chose the {self.dice[computer_dice_idx].values} dice")

        user_roll, computer_roll = self.execute_rounds(
            user_first, user_dice_idx, computer_dice_idx
        )

        self.declare_winner(user_roll, computer_roll)

    def get_user_guess(self):
        while True:
            user_guess = (
                input(
                    "Try to guess my selection.\n0 - 0\n1 - 1\nx - exit\n? - help\nYour selection: "
                )
                .strip()
                .lower()
            )
            if user_guess in ["0", "1"]:
                return user_guess
            elif user_guess == "x":
                sys.exit("Game exited.")
            elif user_guess == "?":
                probabilities = ProbabilityCalculator.calculate_win_probabilities(
                    [d.values for d in self.dice]
                )
                HelpMenu.display_help([d.values for d in self.dice], probabilities)
            else:
                print("Invalid selection. Try again.")

    def get_computer_dice_selection(self):
        return random.choice(
            [i for i in range(len(self.dice)) if i not in self.used_dice]
        )

    def execute_rounds(self, user_first, user_dice_idx, computer_dice_idx):
        if user_first:
            user_roll = self.perform_turn(user_dice_idx, is_user=True)
            computer_roll = self.perform_turn(computer_dice_idx, is_user=False)
        else:
            computer_roll = self.perform_turn(computer_dice_idx, is_user=False)
            user_roll = self.perform_turn(user_dice_idx, is_user=True)
        return user_roll, computer_roll

    def perform_turn(self, dice_idx, is_user):
        computer_num, computer_hmac, computer_key = self.roll()
        if is_user:
            print(
                f"It's time for your throw.\nI selected a random value in the range 0..5\n(HMAC={computer_hmac})"
            )
        else:
            print(
                f"It's time for my throw.\nI selected a random value in the range 0..5\n(HMAC={computer_hmac})"
            )
        modulus, user_num = Modulator.module(computer_num, self.dice)
        print(
            f"My number is {computer_num}\n(KEY={computer_key.hex()})\nThe result is {computer_num} + {user_num} = {modulus} (mod 6)."
        )
        if is_user:
            print(f"Your throw is {self.dice[dice_idx].values[modulus]}.")
        else:
            print(f"My throw is {self.dice[dice_idx].values[modulus]}.")
        return self.dice[dice_idx].values[modulus]

    def declare_winner(self, user_roll, computer_roll):
        if user_roll > computer_roll:
            print(f"You win ({user_roll} > {computer_roll})!")
        elif user_roll < computer_roll:
            print(f"I win ({computer_roll} > {user_roll})!")
        else:
            print(f"It's a tie ({user_roll} = {computer_roll})!")


if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise ValueError(
                "No dice configurations provided. Example: python game.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3"
            )

        dice = DiceParser.parse(sys.argv[1:])
        game = DiceGame(dice)
        game.play()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
