import requests
import random
import re
import time
from colorama import init, Fore

# Initialize colorama
init()

VALID_CODES_FILE = 'valid_codes.txt'
INVALID_CODES_FILE = 'invalid_codes.txt'

def extract_code(url):
    """Extract the 24-character random code from the URL."""
    match = re.search(r'[a-zA-Z0-9]{24}', url)
    if match:
        return match.group(0)
    else:
        return None

def send_request_and_process_code(code, webhook_url):
    """Send a GET request and process the response code."""
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Code {Fore.CYAN}{code}{Fore.RESET} > Status: {Fore.GREEN}VALID{Fore.RESET}")
        send_to_discord_webhook(code, webhook_url)
        save_to_file(code, VALID_CODES_FILE)
    elif response.status_code == 429:  # Rate limit exceeded
        retry_after = response.json().get("retry_after") / 1000  # Convert to seconds
        print(f"{Fore.RED}Rate limited. Waiting for {retry_after} seconds before retrying...{Fore.RESET}")
        time.sleep(retry_after)
        send_request_and_process_code(code, webhook_url)  # Retry the request
    else:
        print(f"Code {Fore.CYAN}{code}{Fore.RESET} > Status: {Fore.RED}INVALID{Fore.RESET}")
        save_to_file(code, INVALID_CODES_FILE)

def send_to_discord_webhook(code, webhook_url):
    """Send the code to Discord webhook."""
    data = {
        "username": "NitroBotz",
        "content": f"https://discord.gift/{code}"
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"{Fore.RED}Failed to send message to Discord webhook: {response.status_code}{Fore.RESET}")

def save_to_file(code, filename):
    """Save the code to a text file."""
    with open(filename, 'a') as f:
        f.write(f"https://discord.gift/{code}\n")

def print_banner():
    """Print a fancy ASCII art banner."""
    banner = """
,-.        .  .         ,   
|  \ o     |  |         |   
|  | . ,-. |--| ,-. ,-. | , 
|  / | `-. |  | | | | | |<  
`-'  ' `-' '  ' `-' `-' ' ` 
    """
    print(f"{Fore.CYAN}{banner}{Fore.RESET}")

if __name__ == "__main__":
    print_banner()
    print(f"{Fore.MAGENTA}ChatGPT's Discord Nitro Checker \n{Fore.RESET}")
    webhook_url = input(f"{Fore.YELLOW}Enter your Discord webhook URL: {Fore.RESET}")
    codes_file = input(f"{Fore.YELLOW}Enter codes filelist: {Fore.RESET}")
    print(f"Checking codes from {Fore.MAGENTA}{codes_file}{Fore.RESET}... | Result will be saved to {Fore.GREEN}valid_codes.txt{Fore.RESET}")
    with open(codes_file, 'r') as f:
        urls = f.read().splitlines()
    for url in urls:
        code = extract_code(url)
        if code:
            send_request_and_process_code(code, webhook_url)
            delay = random.uniform(10, 20)  
            print(f"{Fore.YELLOW}Delay {delay} seconds as needed to avoid rate limiting{Fore.RESET}")
            time.sleep(delay)
        else:
            print(f"{Fore.RED}No code found in URL: {url}{Fore.RESET}")
