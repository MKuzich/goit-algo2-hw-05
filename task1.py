import hashlib

class BloomFilter:
    def __init__(self, size: int, num_hashes: int):
        self.size = size
        self.num_hashes = num_hashes
        self.bit_array = [0] * size

    def _hashes(self, item: str):
        hashes = []
        for i in range(self.num_hashes):
            data = f"{item}-{i}".encode('utf-8')
            hash_digest = hashlib.md5(data).hexdigest()
            hash_int = int(hash_digest, 16)
            hashes.append(hash_int % self.size)
        return hashes

    def add(self, item: str):
        if not isinstance(item, str) or not item:
            return
        for index in self._hashes(item):
            self.bit_array[index] = 1

    def __contains__(self, item: str):
        if not isinstance(item, str) or not item:
            return False
        return all(self.bit_array[index] for index in self._hashes(item))

def check_password_uniqueness(bloom_filter: BloomFilter, passwords: list):
    result = {}
    for password in passwords:
        if not isinstance(password, str) or not password:
            result[password] = "некоректне значення"
        elif password in bloom_filter:
            result[password] = "вже використаний"
        else:
            result[password] = "унікальний"
            bloom_filter.add(password)
    return result

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
