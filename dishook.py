import requests
import random
import string
import time
from colorama import init, Fore

# Initialize colorama
init()

VALID_CODES_FILE = 'valid_codes.txt'
INVALID_CODES_FILE = 'invalid_codes.txt'

def generate_random_string(length=24):
    """Generate a random alphanumeric string of specified length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def send_request_and_process_code(code, webhook_url):
    """Send a GET request and process the response code."""
    url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{code}?with_application=false&with_subscription_plan=true"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Code {Fore.CYAN}{code}{Fore.RESET} > Status: {Fore.GREEN}VALID{Fore.RESET}")
        send_to_discord_webhook(code, webhook_url)
        save_to_file(code, VALID_CODES_FILE)
        print(f"{Fore.YELLOW}Delay 10 seconds as needed to avoid rate limiting{Fore.RESET}")
    elif response.status_code == 429:  # Rate limit exceeded
        retry_after = response.json().get("retry_after") / 1000  # Convert to seconds
        print(f"{Fore.RED}Rate limited. Waiting for {retry_after} seconds before retrying...{Fore.RESET}")
        time.sleep(retry_after)
        send_request_and_process_code(code, webhook_url)  # Retry the request
    else:
        print(f"Code {Fore.CYAN}{code}{Fore.RESET} > Status: {Fore.RED}INVALID{Fore.RESET}")
        save_to_file(code, INVALID_CODES_FILE)
        print(f"{Fore.YELLOW}Delay 10 seconds as needed to avoid rate limiting{Fore.RESET}")

def send_to_discord_webhook(code, webhook_url):
    """Send the code to Discord webhook."""
    data = {
        "content": f"https://discord.gift/{code}"
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code != 200:
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
    print(f"{Fore.MAGENTA}ChatGPT's Discord Nitro Generator \n{Fore.RESET}")
    webhook_url = input(f"{Fore.YELLOW}Enter your Discord webhook URL: {Fore.RESET}")
    delay = float(input(f"{Fore.YELLOW}Enter delay time (to avoid rate limiting): {Fore.RESET}"))
    print(f"Generated {Fore.MAGENTA}Code{Fore.RESET} will be saved to: {Fore.GREEN}valid_codes.txt{Fore.RESET}")
    while True:
        random_code = generate_random_string()
        send_request_and_process_code(random_code, webhook_url)
        time.sleep(delay)  # Adjust the delay as needed to avoid rate limiting
