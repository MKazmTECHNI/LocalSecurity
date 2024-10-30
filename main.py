import requests
from os import getcwd

url = "https://raw.githubusercontent.com/MKazmTECHNI/LocalSecurity/main/main.py"
directory = getcwd()
filename = f"{directory}/safety.py"

response = requests.get(url)

with open(filename, "w") as f:
    f.write(response.text)  # `.text` gives a string format instead of bytes
f.close()
