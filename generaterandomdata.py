from datetime import datetime, timedelta
import random
import json

class GenerateRandomFlights:
    def __init__(self, random_data_json_file='./random_data.json'):
        self.alphabet = [chr(point_code) for point_code in range(ord('A'), ord('Z') + 1)]
        with open(random_data_json_file) as f:
            self.random_data_dict = json.load(f)

    def generateRandomFlightCode(self):
        random_flight_code = ''
        for num in range(random.randint(2, 3)):
            random_flight_code += random.choice(self.alphabet)
        for num in range(3):
            random_flight_code += str(random.randint(0, 9))
        return random_flight_code

    def generateRandomGate(self):
        random_gate = ''
        random_gate += self.alphabet[random.randint(0, 5)] # A-F
        for num in range(2):
            random_gate += str(random.randint(0, 9))
        return random_gate

    def generateRandomTime(self):
        current_time = datetime.now() 
        result_time = current_time + timedelta(minutes=random.randint(1,10))
        return int(result_time.strftime('%H%M'))

    def getRandomDestination(self):
        return random.choice(self.random_data_dict['destinations_origins'])

    def getRandomOrigin(self):
        return random.choice(self.random_data_dict['destinations_origins'])

    def getRandomStatus(self):
        return random.choice(self.random_data_dict['status'])

    def getRandomAirline(self):
        return random.choice(self.random_data_dict['airlines']) 
