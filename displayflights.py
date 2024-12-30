from datetime import datetime
import sqlite3
import signal
import sys
from time import sleep, time as _time
from os import system, remove, path, get_terminal_size, name as _os_name
import logging
import argparse
sys.path.append('./auxiliary')

import managedatabase
from auxiliary import loadingmotions
from auxiliary import generaterandomdata
from auxiliary.formattime import formatTime

# Constants
ARRIVALS = 'arrivals'
DEPARTURES = 'departures'

def handler(signum, frame):
    sys.stderr.write('\n\n[ + ] Exiting...\n\n')
    exit(1)

signal.signal(signal.SIGINT, handler)

parser = argparse.ArgumentParser()
parser.add_argument("--test", help="test mode. This creates a database with random data for demo purposes",
                    action="store_true")
args = parser.parse_args()

class FlightTimeTableTerminal:
    def displayFlights(self, databasefile:str, stty_size:tuple) -> None:
    # display arrivals and departures
        epoch = int(datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute).timestamp())
        if _os_name == 'nt':
            system('cls')
        else:
            system('clear')
        for counter, table in enumerate((ARRIVALS, DEPARTURES)):
            tables = managedatabase.FlightsManager(databasefile=databasefile).getCurrentArrivals(epoch) if not counter else \
                    managedatabase.FlightsManager(databasefile=databasefile).getCurrentDepartures(epoch)
            table_columns = managedatabase.FlightsManager().getColumns(table) 
            print(f'{table}'.upper().center(stty_size[0], '-'))
            # Display columns but not index column
            space = int(stty_size[0] / len(table_columns))
            for result in table_columns[1:]:
                column_name = result[1]
                if column_name == 'flight_code':
                    column_name = 'flight code'
                print(column_name.ljust(space).title(), end='')
            print()
            # Display rows from tables with format
            for result in tables[:10 if len(tables) > 10 else len(tables)]:
                flight_time = result[3]
                for indx in range(1, len(result)):
                    data = result[indx]
                    if isinstance(data, int):
                        data = formatTime(data)
                    print(data.ljust(space), end='')
                print('')
            print('\n\n')
        sleep(1)

def main() -> None:
    if args.test:
        databasefile = 'testflights.db'
        if path.exists(f'./{databasefile}'):
            remove(databasefile)
        print('[ + ] Test mode is on')
        print(f'[ + ] Initializing database {databasefile} with random data')
        loadingmotions.loadingMotion()
        managedatabase.initializeDatabase(databasefile)
        logging.info('Inserting data into tables')
        total_rows = 0
        while total_rows < 1000:
            for tablename in [ARRIVALS, DEPARTURES]:
                managedatabase.insertRandomData(tablename)
                total_rows += 1
    else:
        databasefile = 'flights.db'
    if managedatabase.FlightsManager(databasefile=databasefile).isEmpty():
        print('You can create a database with managedatabase.py program or use the flag --test to create a database with random data for a demo')
        parser.print_help()
        exit(1)
    while True:
        stty_size = get_terminal_size()
        FlightTimeTableTerminal().displayFlights(databasefile=databasefile, stty_size=stty_size)
        sleep(30)

if __name__ == '__main__':
    main()
