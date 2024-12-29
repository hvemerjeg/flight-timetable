from datetime import datetime, timedelta
import random
import time

class GenerateRandomFlights:
    random_data_dict = {
            "destinations_origins": ["Santo Domingo", "New York", "Los Angeles", "London", "Tokyo", "Paris", "Dubai", "Singapore", "Hong Kong", "Sydney", "Berlin", "Rome", "Istanbul", "Moscow", "Toronto", "Beijing", "Bangkok", "San Francisco", "Mexico City", "São Paulo", "Buenos Aires", "Chicago", "Vancouver", "Johannesburg", "Cape Town", "Madrid", "Lisbon", "Barcelona", "Vienna", "Munich", "Melbourne", "Seoul", "Shanghai", "Delhi", "Mumbai", "Kuala Lumpur", "Jakarta", "Brussels", "Amsterdam", "Copenhagen", "Stockholm", "Oslo", "Helsinki", "Warsaw", "Prague", "Budapest", "Athens", "Dublin", "Reykjavik", "Doha", "Abu Dhabi", "Riyadh", "Casablanca", "Cairo", "Lima", "Bogotá", "Caracas", "Havana", "San Jose", "Panama City", "Manila", "Taipei", "Bangladesh", "Ho Chi Minh City", "Phnom Penh", "Hanoi", "Yangon", "Colombo", "Malé", "Auckland", "Christchurch", "Perth", "Brisbane", "Darwin", "Adelaide", "San Diego", "Phoenix", "Dallas", "Houston", "Seattle", "Miami", "Las Vegas", "Atlanta", "Boston", "Denver", "Philadelphia", "Montreal", "Edmonton", "Ottawa", "Quebec City", "Guadalajara", "Monterrey", "Santiago", "Quito", "La Paz", "Asunción", "Montevideo", "Brasília", "Porto Alegre", "Recife", "Salvador", "Fortaleza"], 
            "airlines": ["ANA", "Asiana", "Egyptair", "Finnair", "flydubai", "Iberia", "Icelandair", "Jetstar", "KLM", "Lufthansa", "Luxair", "Peach", "RwandAir", "Ryanair", "SpiceJet"], 
            "airlines_codes": ["NH", "OZ", "MS", "AY", "FZ", "IB", "FI", "JQ", "KL", "LH", "LG", "MM", "WB", "FR", "SG"], 
            "status": ["on-time", "delayed", "cancelled"]}

    alphabet = [chr(point_code) for point_code in range(ord('A'), ord('F') + 1)]
    random_indx = random.randint(1, len(random_data_dict['airlines']) - 1)
    random_num = random.randint(60, 2 * 60)

    def generateRandomFlightCode(self):
        # This function needs to be call before the getRandomAirline function
        random_flight_code = GenerateRandomFlights.random_data_dict['airlines_codes'][GenerateRandomFlights.random_indx]
        for num in range(3):
            random_flight_code += str(random.randint(0, 9))
        return random_flight_code

    def generateRandomGate(self):
        random_gate = ''
        random_gate += GenerateRandomFlights.alphabet[random.randint(0, 5)]
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
        # This functions should be called after generateRandomFlightCode function
        random_indx = GenerateRandomFlights.random_indx
        GenerateRandomFlights.random_indx = random.randint(1, len(GenerateRandomFlights.random_data_dict['airlines']) - 1)
        return GenerateRandomFlights.random_data_dict['airlines'][random_indx]
