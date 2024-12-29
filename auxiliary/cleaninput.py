import re
import sys

def cleanInput(user_input:str, allow_char):
    # Allow letters, numbers, spaces 
    if len(user_input) > 25:
        sys.stderr.write('Input exceeds maximum allowed length.\n')
        exit(1)
    if allow_char == 'space':
        cleaned_input = re.sub(r'[^a-zA-Z0-9\s]', '', user_input)
    elif allow_char == 'hyphen':
        cleaned_input = re.sub(r'[^a-zA-Z0-9\-]', '', user_input)
    else:
        cleaned_input = re.sub(r'[^a-zA-Z0-9]', '', user_input)
    return cleaned_input
