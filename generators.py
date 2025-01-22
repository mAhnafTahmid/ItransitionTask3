import hmac
import secrets
import hashlib


class SecureRandom:
    @staticmethod
    def generate_key() -> bytes:
        return secrets.token_bytes(32)  # 256-bit key

    @staticmethod
    def generate_hmac(key: bytes, message: str) -> str:
        return hmac.new(key, message.encode(), hashlib.sha3_256).hexdigest()

    @staticmethod
    def secure_random_number(max_value: int) -> int:
        while True:
            num = secrets.randbelow(max_value + 1)
            if 0 <= num <= max_value:
                return num
