from colorama import Fore

with open('config.py', 'r', encoding='utf-8-sig') as file:
    module_config = file.read()

exec(module_config)

with open('wallets.txt', 'r', encoding='utf-8-sig') as file:
    mnemonics = [line.strip() for line in file]

with open('proxies.txt', 'r', encoding='utf-8-sig') as file:
    proxies = [line.strip() for line in file]
    if not proxies:
        proxies = [None for _ in range(len(mnemonics))]

print(Fore.BLUE + f'Loaded {len(mnemonics)} wallets:')
print('\033[39m')
