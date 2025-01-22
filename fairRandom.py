from typing import Tuple
from generators import SecureRandom


class FairRandomProtocol:
    @staticmethod
    def generate_and_prove(max_value: int) -> Tuple[int, str, bytes]:
        key = SecureRandom.generate_key()
        number = SecureRandom.secure_random_number(max_value)
        hmac_value = SecureRandom.generate_hmac(key, str(number))
        return number, hmac_value, key
