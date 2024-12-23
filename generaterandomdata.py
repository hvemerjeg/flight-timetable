from datetime import datetime, timedelta
import random
import json
import time

class GenerateRandomFlights:
    random_data_json_file = './random_data.json'
    alphabet = [chr(point_code) for point_code in range(ord('A'), ord('Z') + 1)]
    with open(random_data_json_file) as f:
        random_data_dict = json.load(f)
    random_indx = random.randint(1, len(random_data_dict['airlines']) - 1)
    random_num = random.randint(60, 2 * 60)

    def generateRandomFlightCode(self):
        random_flight_code = GenerateRandomFlights.random_data_dict['airlines_codes'][GenerateRandomFlights.random_indx]
        for num in range(3):
            random_flight_code += str(random.randint(0, 9))
        return random_flight_code

    def generateRandomGate(self):
        random_gate = ''
        random_gate += GenerateRandomFlights.alphabet[random.randint(0, 5)] # A-F
        for num in range(2):
            random_gate += str(random.randint(0, 9))
        return random_gate

    def generateRandomTime(self):
        current_time = time.time()
        result_time = current_time + GenerateRandomFlights.random_num
        GenerateRandomFlights.random_num += random.randint(60, 5 * 60)
        return int(result_time)

    def getRandomDestination(self):
        return random.choice(GenerateRandomFlights.random_data_dict['destinations_origins'])

    def getRandomOrigin(self):
        return random.choice(GenerateRandomFlights.random_data_dict['destinations_origins'])

    def getRandomStatus(self):
        return random.choice(GenerateRandomFlights.random_data_dict['status'])

    def getRandomAirline(self):
        random_indx = GenerateRandomFlights.random_indx
        GenerateRandomFlights.random_indx = random.randint(1, len(GenerateRandomFlights.random_data_dict['airlines']) - 1)
        return GenerateRandomFlights.random_data_dict['airlines'][random_indx]
