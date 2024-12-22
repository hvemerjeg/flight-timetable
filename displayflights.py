from datetime import datetime, time
import sqlite3
import signal
import sys
from time import sleep
from os import system, remove, path
import logging
import argparse

import managedatabase
import loadingmotions
import generaterandomdata

# Constants
ARRIVALS = 'arrivals'
DEPARTURES = 'departures'

def handler(signum, frame):
    sys.stderr.write('\n\n[ + ] Exiting...\n\n')
    exit(1)

signal.signal(signal.SIGINT, handler)

parser = argparse.ArgumentParser()
parser.add_argument("--test", help="Test mode. This creates a database with random data for demo purposes",
                    action="store_true")
args = parser.parse_args()

def initializeDatabase(database_file):
    managedatabase.FlightsManager(database_file)
    managedatabase.FlightsManager().createTable(ARRIVALS)
    managedatabase.FlightsManager().createTable(DEPARTURES)

def insertRandomData(tablename:str):
        # Insert random data in case that the database is empty
        random_flight_code = generaterandomdata.GenerateRandomFlights().generateRandomFlightCode()
        random_gate = generaterandomdata.GenerateRandomFlights().generateRandomGate()
        random_status = generaterandomdata.GenerateRandomFlights().getRandomStatus()
        random_airline = generaterandomdata.GenerateRandomFlights().getRandomAirline()
        random_time = generaterandomdata.GenerateRandomFlights().generateRandomTime()

        if tablename == DEPARTURES:
            random_destination = generaterandomdata.GenerateRandomFlights().getRandomDestination()
            managedatabase.FlightsManager().insertFlight(tablename, (random_flight_code, random_destination,\
                random_time, random_gate, random_status, random_airline))
        elif tablename == ARRIVALS:
            random_origin = generaterandomdata.GenerateRandomFlights().getRandomOrigin()
            managedatabase.FlightsManager().insertFlight(tablename, (random_flight_code, random_origin,\
                random_time, random_gate, random_status, random_airline))

def adjustTime(time:str):
    if len(time) < 4:
        time = '0' + time
    if len(time) < 4:
        time = time + '0'
    return f'{time[:2]}:{time[2:]}'

class FlightTimeTableTerminal:
    def displayFlights(self) -> None:
    # display arrivals and departures
        system('clear')
        for counter, table in enumerate((ARRIVALS, DEPARTURES)):
            tables = managedatabase.FlightsManager().getCurrentArrivals(int(datetime.now().strftime('%H%M'))) if not counter else \
                    managedatabase.FlightsManager().getCurrentDepartures(int(datetime.now().strftime('%H%M')))
            table_columns = managedatabase.FlightsManager().getColumns(table) 
            print(f'{table}'.upper().center(150, '-'))
            # Display columns but not index column
            for result in table_columns:
                column_name = result[1]
                if column_name == 'id':
                    continue
                elif column_name == 'flight_code':
                    column_name = 'flight code'
                print(column_name.ljust(20).title(), end='')
            print()
            # Display rows from tables with format
            tables.sort(key=lambda x: x[3])
            for result in tables[:10 if len(tables) > 10 else len(tables)]:
                flight_time = result[3]
                for indx in range(1, len(result)):
                    data = result[indx]
                    if isinstance(data, int):
                        data = str(data)
                        data = adjustTime(data)
                    print(data.ljust(20), end='') # Data from the database can be an integer type
                print('')
            print('\n\n')
        sleep(1)

def main():
    if args.test:
        database_file = 'flights.db'
        if path.exists(f'./{database_file}'):
            remove(database_file)
        print('[ + ] Test mode is on')
        print('[ + ] Initializing database with random data')
        loadingmotions.loadingMotion()
        initializeDatabase(database_file)
        logging.info('Inserting data into tables')
        for tablename in [ARRIVALS, DEPARTURES]:
            for num in range(20):
                insertRandomData(tablename)
    while True:
        FlightTimeTableTerminal().displayFlights()
        sleep(30)


if __name__ == '__main__':
    main()
