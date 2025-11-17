# importing libraries
import requests, threading

# defining domain and list to store discovered subdomains
domain = "youtube.com"
discovered_subdomains = []

# lock for thread-safe operations
lock = threading.Lock()

# loading subdomains from file
with open("subdomains.txt", "r") as file:
    subdomains = file.read().splitlines()

# function to check subdomains and append discovered ones
def check_subdomain(sub):
    url = f"http://{sub}.{domain}"
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            with lock:
                discovered_subdomains.append(url)
                print(f"Discovered: {url}")
    except requests.RequestException:
        print(f"Not Found: {url}")

# creating and starting threads for each subdomain
threads = []

for sub in subdomains:
    thread = threading.Thread(target=check_subdomain, args=(sub,))
    threads.append(thread)
    thread.start()

# waiting for all threads to complete
for thread in threads:
    thread.join()

# writing discovered subdomains to a file
with open("discovered_subdomains.txt", "w") as output_file:
    for subdomain in discovered_subdomains:
        output_file.write(subdomain + "\n")
