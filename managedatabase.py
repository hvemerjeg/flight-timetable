import sqlite3
from os import path, system, remove, get_terminal_size, name as _os_name
import sys
from time import time as _time, sleep
import random
from datetime import datetime, timedelta
import re
import signal
import argparse
import glob
sys.path.append('./auxiliary')

from auxiliary import consultairlineflightcode
from auxiliary.formattime import formatDateTime
from auxiliary import generaterandomdata
from auxiliary import loadingmotions
from auxiliary import cleaninput

# Constants
ARRIVALS = 'arrivals'
DEPARTURES = 'departures'


def initializeDatabase(databasefile:str) -> None:
    FlightsManager(databasefile)
    FlightsManager(databasefile).createTable(ARRIVALS)
    FlightsManager(databasefile).createTable(DEPARTURES)

def insertRandomData(tablename:str) -> None:
        # Insert random data in case that the database is empty
        random_flight_code = generaterandomdata.GenerateRandomFlights().generateRandomFlightCode()
        random_gate = generaterandomdata.GenerateRandomFlights().generateRandomGate()
        random_status = generaterandomdata.GenerateRandomFlights().getRandomStatus()
        random_airline = generaterandomdata.GenerateRandomFlights().getRandomAirline()
        random_time = generaterandomdata.GenerateRandomFlights().generateRandomTime()

        if tablename == DEPARTURES:
            random_destination = generaterandomdata.GenerateRandomFlights().getRandomDestination()
            FlightsManager().insertFlight(tablename, (random_flight_code, random_destination,\
                random_time, random_gate, random_status, random_airline))
        elif tablename == ARRIVALS:
            random_origin = generaterandomdata.GenerateRandomFlights().getRandomOrigin()
            FlightsManager().insertFlight(tablename, (random_flight_code, random_origin,\
                random_time, random_gate, random_status, random_airline))

class FlightsManager:
    def __init__(self, databasefile='./testflights.db'):
        self.databasefile = databasefile
        self.conn = sqlite3.connect(self.databasefile)
        self.cursor = self.conn.cursor()

    def isEmpty(self) -> bool:
        departures_table = self.cursor.execute('SELECT name FROM sqlite_master WHERE type = "table" AND name = "departures"').fetchall()
        arrivals_table = self.cursor.execute('SELECT name FROM sqlite_master WHERE type = "table" AND name = "arrivals"').fetchall()
        if not departures_table or not arrivals_table:
            sys.stderr.write('The database with flight information (departures or arrivals) might be empty\n')
            return True
        return False

    def backupAndClean(self):
        backup_files = glob.glob(f'./{self.databasefile}.bak_*')
        if backup_files:
            backup_files.sort(key=path.getmtime, reverse=True)
            newest_backup = backup_files[0]
            date_of_backup = newest_backup.split('_')[1].split('-')
        # A backup is made each month
        if not backup_files or datetime(int(date_of_backup[0]), int(date_of_backup[1]), int(date_of_backup[2])) < \
                datetime(datetime.now().year, datetime.now().month, datetime.now().day) - timedelta(days=31): 
            current_date_time = datetime(datetime.now().year, datetime.now().month, datetime.now().day)
            current_date_time_formatted = current_date_time.strftime('%Y-%m-%d_%H-%M-%S')
            # backup
            print(f'[ + ] Backing up database\nThis can take a while depending on the size of the database\n')
            if _os_name == 'nt':
                system(f'copy {self.databasefile} {self.databasefile}.bak_{current_date_time_formatted}')
            else:
                system(f'cp {self.databasefile} {self.databasefile}.bak_{current_date_time_formatted}')
            # delete flights that are 31 or more days old
            self.cursor.execute('DELETE FROM arrivals WHERE time <= ?', (int(current_date_time.timestamp()) - 2678400, ))
            self.cursor.execute('DELETE FROM departures WHERE time <= ?', (int(current_date_time.timestamp()) - 2678400, ))
            if backup_files:
                remove(newest_backup)

    def createTable(self, tablename:str) -> None:
        if tablename == DEPARTURES:
            self.cursor.execute(f'CREATE TABLE {DEPARTURES}(id INTEGER PRIMARY KEY, flight_code TEXT NOT NULL, destination TEXT NOT NULL, time INTEGER NOT NULL, gate TEXT NOT NULL, status TEXT NOT NULL, airline TEXT NOT NULL);')
        elif tablename == ARRIVALS:
            self.cursor.execute(f'CREATE TABLE {ARRIVALS}(id INTEGER PRIMARY KEY, flight_code TEXT NOT NULL, origin TEXT NOT NULL, time INTEGER NOT NULL, gate TEXT NOT NULL, status TEXT NOT NULL, airline TEXT NOT NULL);')

    def updateFlightTime(self, tablename:str, flight_code:str, new_time:str, flight_time:str) -> None:
        if tablename == ARRIVALS or tablename == DEPARTURES:
            self.cursor.execute(f'UPDATE {tablename} SET time = ? WHERE flight_code = ? AND time = ?;', (new_time, flight_code, flight_time))
            self.conn.commit()

    def updateFlightStatus(self, tablename:str, flight_code:str, status:str, flight_time:str) -> None:
        if tablename == ARRIVALS or tablename == DEPARTURES:
            self.cursor.execute(f'UPDATE {tablename} SET status = ? WHERE flight_code = ? AND time = ?;', (status, flight_code, flight_time))
            self.conn.commit()

    def updateFlightGate(self, tablename:str, flight_code:str, flight_gate:str, flight_time:str) -> None:
        if tablename == ARRIVALS or tablename == DEPARTURES:
            self.cursor.execute(f'UPDATE {tablename} SET gate = ? WHERE flight_code = ? AND time = ?', (flight_gate, flight_code, flight_time))
            self.conn.commit()

    def getFlight(self, tablename:str, flight_code:str, flight_time:str) -> list[tuple]:
        if tablename == ARRIVALS or tablename == DEPARTURES:
            return self.cursor.execute(f'SELECT * FROM {tablename} WHERE flight_code = ? AND time = ?;', (flight_code, flight_time)).fetchall()

    def getAllArrivals(self) -> list[tuple]:
        return self.cursor.execute(f'SELECT * FROM {ARRIVALS} ORDER BY time ASC;').fetchall()

    def getAllDepartures(self) -> list[tuple]:
        return self.cursor.execute(f'SELECT * FROM {DEPARTURES} ORDER BY time ASC;').fetchall()

    def getCurrentArrivals(self, current_time:int) -> list[tuple]:
        epoch = int(datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute).timestamp())
        if isinstance(current_time, int): 
            return self.cursor.execute(f'SELECT * FROM {ARRIVALS} WHERE time >= ? AND time <= ? ORDER BY time ASC', (current_time, \
                    epoch + 86400)).fetchall()

    def getCurrentDepartures(self, current_time:int) -> list[tuple]:
        epoch = int(datetime(datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute).timestamp())
        if isinstance(current_time, int): 
            return self.cursor.execute(f'SELECT * FROM {DEPARTURES} WHERE time >= ? AND time <= ? ORDER BY time ASC', (current_time, \
                    epoch + 86400)).fetchall()

    def deleteFlight(self, tablename:str, flight_code:tuple, flight_time:str) -> None:
        self.cursor.execute(f'DELETE FROM {tablename} WHERE flight_code = ? AND time = ?', (flight_code, flight_time)) 
        self.conn.commit()

    def insertFlight(self, tablename:str, data_to_insert:tuple) -> None:
        if tablename == ARRIVALS:
            self.cursor.execute(f'INSERT INTO {tablename}(flight_code, origin, time, gate, \
                    status, airline) VALUES(?, ?, ?, ?, ?, ?)', data_to_insert)
        elif tablename == DEPARTURES:
            self.cursor.execute(f'INSERT INTO {tablename}(flight_code, destination, time, gate, \
                    status, airline) VALUES(?, ?, ?, ?, ?, ?)', data_to_insert)
        self.conn.commit()
    
    def getColumns(self, tablename:str) -> list[tuple]:
        if tablename == ARRIVALS or tablename == DEPARTURES:
            return self.cursor.execute(f'PRAGMA table_info({tablename})').fetchall()

def main():
    def isValidDate(year:int, month:int, day:int, hours:int, minutes:int) -> bool:
        try:
            datetime(year, month, day, hours, minutes)
        except (TypeError, ValueError):
            print(f'The given date: {year}-{month}-{day} is invalid')
            return False
        
        # The date of the flight must be between now and one year in the future
        if not datetime(datetime.now().year, datetime.now().month, datetime.now().day) <= datetime(year, month, day) \
                <= datetime(datetime.now().year+1, datetime.now().month, datetime.now().day):
            print(f'The date of the flight must be between now and one year in the future')
            return False
        return True

    def isValidFlightCode(airline:str, flight_code:str) -> bool:
        result = consultairlineflightcode.getFlightCode(airline) 
        if not result:
           sys.stderr.write('No codes where found for the specified airline.\n') 
           sys.stderr.write('This may be because the airline is not valid or yet registered.\n')
           exit(1)
        letters_of_code = ''
        for char in flight_code:
            if char.isalpha() and len(letters_of_code) < 6:
                letters_of_code += char
            else:
                break
        if letters_of_code not in result:
            sys.stderr.write(f'The code starting with {letters_of_code} is not valid code for the airline: {airline}\nThe list of two-letter codes for {airline} is the following: {result}\n')
            return False
        return True
    
    def _confirmation(dataname:str, data):
        confirmation = input(f'Is this correct?\n{dataname} -> {data}\nInsert Y or N: ').upper()
        return confirmation

    def getGeneralInput(message:str, valid_options:tuple, dataname:str):
        user_input = input(message).lower()
        user_input = cleaninput.cleanInput(user_input, allow_char='hyphen') if user_input.strip() == 'on-time' \
                else cleaninput.cleanInput(user_input, allow_char=None)
        confirmation = _confirmation(dataname, user_input)
        while user_input not in valid_options or confirmation != 'Y':
            user_input = input(f'You need to choose between {valid_options}: ')
            user_input = cleaninput.cleanInput(user_input, allow_char='hyphen') if user_input.strip() == 'on-time' \
                else cleaninput.cleanInput(user_input, allow_char=None)
            confirmation = _confirmation(dataname, user_input)
        return user_input

    def getFlightCode(airline:str) -> str:
        flight_code = ''
        confirmation = None
        is_valid_flight_code = None
        while (len(flight_code) < 3 or len(flight_code) > 6) or confirmation != 'Y' or not is_valid_flight_code:
            flight_code = input('Insert flight code (minimum of 3 characters and maximum of 6 characters): ').upper()
            flight_code = cleaninput.cleanInput(flight_code, allow_char=None)
            confirmation = _confirmation('flight code', flight_code)
            is_valid_flight_code = isValidFlightCode(airline, flight_code)
        return flight_code

    def getFlightTime(current_or_new:str):
        message1 = 'Insert flight date and time in the format of YYYY-MM-DD HH:MM: ' 
        message2 = 'Insert new flight date and time in the format of YYYY-MM-DD HH:MM: '
        message3 = 'flight date and time: '
        message4 = 'New flight date and time: '
        confirmation = None
        is_valid_date = None
        while confirmation != 'Y' or not is_valid_date:
            flight_date_time = input(message1) if current_or_new == 'current' else input(message2)
            flight_date_time_match = re.search('^[0-9]{4}-(0[0-9]|[1][0-2])-([0-2][0-9]|3[0-1]) ([0-1][0-9]|[2][0-4]):[0-5][0-9]$', flight_date_time)
            confirmation = _confirmation(message3, flight_date_time) if current_or_new == 'current' else _confirmation(message4, flight_date_time)
            if flight_date_time_match:
                flight_date_time_match = flight_date_time_match.group()
                date, time = list(map(int, flight_date_time.split()[0].split('-'))), \
                        list(map(int, flight_date_time.split()[1].split(':')))
                is_valid_date = isValidDate(year=date[0], month=date[1], day=date[2], hours=time[0], minutes=time[1])
            else:
                is_valid_date = False

        flight_date_time_object = datetime.strptime(flight_date_time, '%Y-%m-%d %H:%M')
        flight_date_time_epoch = int(flight_date_time_object.timestamp())
        return flight_date_time_epoch

    def getGate(current_or_new:str):
        # Do not validate gate, because different airports can have different formats
        message1 = 'Insert flight gate: '
        message2 = 'Insert new flight gate: '
        message3 = 'flight gate: '
        message4 = 'New flight gate: '
        confirmation = None
        while confirmation != 'Y':
            flight_gate = input(message1).upper() if current_or_new == 'current' else input(message2).upper()
            flight_gate = cleaninput.cleanInput(flight_gate, allow_char='space')
            confirmation = _confirmation(message3, flight_gate) if current_or_new == 'current' else _confirmation(message4, flight_gate)
        return flight_gate

    def getAirline():
        confirmation = None
        while confirmation != 'Y':
            airline = input('Insert airline: ').title()
            airline = cleaninput.cleanInput(airline, allow_char='space')
            confirmation = _confirmation('airline', airline)
        return airline

    def getOrigin():
        confirmation = None
        while confirmation != 'Y':
            origin = input('Insert origin: ').title()
            origin = cleaninput.cleanInput(origin, allow_char='space')
            confirmation = _confirmation('Origin', origin)
        return origin

    def getDestination():
        confirmation = None
        while confirmation != 'Y':
            destination = input('Insert destination: ').title()
            destination = cleaninput.cleanInput(destination, allow_char='space')
            confirmation = _confirmation('destination', destination).title()
        return destination

    # Global variables
    if args.test:
        databasefile = 'testflights.db'
        if path.exists(f'./{databasefile}'):
            remove(databasefile)
        print('[ + ] Test mode is on')
        print(f'[ + ] Initializing database {databasefile} with random data')
        loadingmotions.loadingMotion()
        initializeDatabase(databasefile)
        total_rows = 0
        while total_rows < 1000:
            for tablename in [ARRIVALS, DEPARTURES]:
                insertRandomData(tablename)
                total_rows += 1
    elif args.init_database:
        databasefile = 'flights.db'
        flight_manager = FlightsManager(databasefile)
        if flight_manager.isEmpty():
            print(f'[ + ] Initializing database {databasefile}')
            initializeDatabase(databasefile)
            print(f'Database {databasefile} was created')
        else:
            print('A database already exists')
        exit(0)
    else:
        databasefile = 'flights.db'
    flight_manager = FlightsManager(databasefile)
    if flight_manager.isEmpty():
        parser.print_help()
        exit(1)
    menu = '\n\n1) Update flight status\n2) Update flight time\n3) Update flight gate\n4) Insert new flight\n5) Delete a flight\n6) Get flight\n7) Display flights\n8) Exit'
    print(menu)
    user_option = input('')
    while user_option != '8':
        if user_option == '1':
            # update flight status
            tablename = getGeneralInput(message='Do you want to update the status of arrivals or departures?: ',\
                    valid_options=('arrivals', 'departures'), dataname='option').lower()
            airline = getAirline()
            flight_code = getFlightCode(airline)
            flight_time = getFlightTime('current')
            status = getGeneralInput(message=f'Insert the new flight status for the flight with code {flight_code}: ',\
                    valid_options=('on-time', 'delayed', 'cancelled'), dataname='status').lower()
            flight_manager.updateFlightStatus(tablename=tablename, flight_code=flight_code, status=status, flight_time=flight_time)
        elif user_option == '2':
            # update flight time
            tablename = getGeneralInput(message='Do you want to update a flight from arrivals or departures?: ',\
                    valid_options=(ARRIVALS, DEPARTURES), dataname='option').lower()
            airline = getAirline()
            flight_code = getFlightCode(airline)
            flight_time = getFlightTime('current')
            new_flight_time = getFlightTime('new')
            flight_manager.updateFlightTime(tablename=tablename, flight_code=flight_code, new_time=new_flight_time, flight_time=flight_time)
        elif user_option == '3':
            # update flight gate
            tablename = getGeneralInput(message='Do you want to update a flight from arrivals or departures?: ',\
                    valid_options=(ARRIVALS, DEPARTURES), dataname='option').lower()
            airline = getAirline()
            flight_code = getFlightCode(airline)
            flight_time = getFlightTime('current')
            gate = getGate('new')
            flight_manager.updateFlightGate(tablename=tablename, flight_code=flight_code, flight_gate=gate, flight_time=flight_time)
        elif user_option == '4':
            # insert flight
            tablename = getGeneralInput(message='Do you want to insert a flight from arrivals or departures?: ',\
                    valid_options=(ARRIVALS, DEPARTURES), dataname='option').lower()
            time = getFlightTime('current')
            gate = getGate('current')
            status = getGeneralInput(message='Insert flight status: ',\
                    valid_options=('on-time', 'delayed', 'cancelled'), dataname='status').lower()
            airline = getAirline()
            flight_code = getFlightCode(airline)
            if tablename == ARRIVALS:
                origin = getOrigin()
                flight_manager.insertFlight(tablename=tablename, data_to_insert=(flight_code, origin, time, gate, status, airline))
            elif tablename == DEPARTURES:
                destination = getDestination()
                flight_manager.insertFlight(tablename=tablename, data_to_insert=(flight_code, destination, time, gate, status, airline))
        elif user_option == '5':
            # delete flight
            tablename = getGeneralInput(message='Do you want to delete a flight from arrivals or departures?: ',\
                    valid_options=('arrivals', 'departures'), dataname='option').lower()
            airline = getAirline()
            flight_code = getFlightCode(airline)
            flight_time = getFlightTime('current')
            flight_manager.deleteFlight(tablename=tablename, flight_code=flight_code, flight_time=flight_time)
        elif user_option == '6':
            # get flight
            tablename = getGeneralInput(message='Do you want to get the flight information from arrivals or departures?: ',\
                    valid_options=(ARRIVALS, DEPARTURES), dataname='option').lower()
            airline = getAirline()
            flight_code = getFlightCode(airline)
            flight_time = getFlightTime('current')
            result = flight_manager.getFlight(tablename=tablename, flight_code=flight_code, flight_time=flight_time)
            if result:
                print()
                stty_size = get_terminal_size()
                space = int(stty_size[0] / len(result[0]))
                for _tuple in result:
                    for element in _tuple[1:]:
                        if isinstance(element, int):
                            element = formatDateTime(element)
                        print(element.ljust(space), end='')
                    print()
                print()
        elif user_option == '7':
            # show flights
            stty_size = get_terminal_size()
            arrivals = flight_manager.getAllArrivals()
            departures = flight_manager.getAllDepartures()
            if arrivals:
                space = int(stty_size[0] / len(arrivals[0]))
            else:
                space = 0
            print('DISPLAYING ALL THE ARRIVALS'.center(stty_size[0], '*'))
            sleep(1)
            for _tuple in arrivals:
                for element in _tuple[1:]:
                    if isinstance(element, int):
                        element = formatDateTime(element)
                    print(element.ljust(space), end='')
                print()
            print()
            if departures:
                space = int(stty_size[0] / len(departures[0]))
            else:
                space = 0
            print('DISPLAYING ALL THE DEPARTURES'.center(stty_size[0], '*'))
            sleep(1)
            for _tuple in departures:
                for element in _tuple[1:]:
                    if isinstance(element, int):
                        element = formatDateTime(element)
                    print(element.ljust(space), end='')
                print()
            print()
        else:
            sys.stderr.write(f'Unrecognized option\n')
            exit(1)
        print(menu)
        user_option = input('')
    if not args.test:
        flight_manager.backupAndClean()
if __name__ == '__main__':
    # SIGNAL.SIGINT handler function
    def handler(signum, frame):
        sys.stderr.write('\n\n[ + ] Exiting...\n\n')
        exit(1)

    signal.signal(signal.SIGINT, handler)

    # argparse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", help="test mode. Create a database with random data for demo purposes",
                        action="store_true")
    parser.add_argument("--init-database", help="Create a database", action="store_true")
    args = parser.parse_args()
    main()
