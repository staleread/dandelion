import bcrypt
import getpass


def generate_password_hash():
    password = getpass.getpass("Enter password to hash: ")

    salt = bcrypt.gensalt(rounds=12)

    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

    print("\n=== Generated Values ===")
    print("Salt (for .env HASH_SALT):")
    print(salt.decode("utf-8"))
    print("\nFull hashed password (for database):")
    print(hashed.decode("utf-8"))
    print("\nExample .env format:")
    print(f"HASH_SALT='{salt.decode('utf-8')}'")


if __name__ == "__main__":
    generate_password_hash()
