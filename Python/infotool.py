import sys
import requests
import socket
import json

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <url>")
    sys.exit()

url = sys.argv[1]

try:
    req = requests.get("https://" + url)
    print("\n" + str(req.headers))
except requests.exceptions.RequestException as e:
    print(f"Error fetching {url}: {e}")
    sys.exit()

try:
    gethostby_ = socket.gethostbyname(url)
    print("\nThe IP Address of " + url + " is " + gethostby_ + "\n")
except socket.error as e:
    print(f"Error resolving {url}: {e}")
    sys.exit()

try:
    req_two = requests.get("https://ipinfo.io/" + gethostby_ + "/json")
    resp_ = json.loads(req_two.text)
    print("location: " + resp_["loc"])
    print("region: " + resp_.get("region", "N/A"))
except requests.exceptions.RequestException as e:
    print(f"Error fetching IP info: {e}")
