import requests
import re
import sys

# Global variables
pattern_airline_codes = r'>[A-Z]{2}<'

def getFlightCode(airline:str) -> str:
    target_url = f'https://www.iata.org/en/publications/directories/code-search/?airline.search={airline}'
    try:
        r = requests.get(target_url)
    except requests.ConnectionError:
        sys.stderr.write('A connection error occurred\nCheck your internet connection.\n')
        exit(1)
    except Exception as e:
        sys.stderr.write(f'{e}\n')
        exit(1)
    airline_codes = re.findall(pattern_airline_codes, r.text)
    if airline_codes:
        airline_codes = list(map(lambda x: x.replace('>', '').replace('<', ''), airline_codes))
        return airline_codes
    else:
        return []
