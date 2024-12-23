import sqlite3
from os import path, system
import sys
from time import sleep
import random
import json
from datetime import datetime, timedelta
import re

import consultairlineflightcode

# Constants
ARRIVALS = 'arrivals'
DEPARTURES = 'departures'

class FlightsManager:
    def __init__(self, databasefile='./test_flights.db'):
        self.databasefile = databasefile
        self.conn = sqlite3.connect(self.databasefile)
        self.cursor = self.conn.cursor()

    def createTable(self, tablename:str) -> None:
        if tablename == DEPARTURES:
            self.cursor.execute(f'CREATE TABLE {DEPARTURES}(id INTEGER PRIMARY KEY NOT NULL, flight_code TEXT NOT NULL, destination TEXT NOT NULL, time INTEGER NOT NULL, gate TEXT NOT NULL, status TEXT NOT NULL, airline TEXT NOT NULL);')
        elif tablename == ARRIVALS:
            self.cursor.execute(f'CREATE TABLE {ARRIVALS}(id INTEGER PRIMARY KEY NOT NULL, flight_code TEXT NOT NULL, origin TEXT NOT NULL, time INTEGER NOT NULL, gate TEXT NOT NULL, status TEXT NOT NULL, airline TEXT NOT NULL);')

    def updateFlightTime(self, tablename:str, flight_code:str, time:str) -> None:
        if tablename == ARRIVALS or tablename == DEPARTURES:
            self.cursor.execute(f'UPDATE {tablename} SET time = "?" WHERE flight_code = "?";', (flight_code, time))
            self.conn.commit()

    def updateFlightStatus(self, tablename:str, flight_code:str, status:str) -> None:
        if tablename == ARRIVALS or tablename == DEPARTURES:
            self.cursor.execute(f'UPDATE {tablename} SET status = "?" WHERE flight_code = "?";', (flight_code, status))
            self.conn.commit()

    def getFlightTime(self, tablename:str, flight_code:str) -> list[tuple]:
        if tablename == ARRIVALS or tablename == DEPARTURES:
            return self.cursor.execute(f'SELECT time FROM {tablename} WHERE flight_code = "?";', (flight_code)).fetchall()

    def getAllArrivals(self) -> list[tuple]:
        return self.cursor.execute(f'SELECT * FROM {ARRIVALS};').fetchall()

    def getAllDepartures(self) -> list[tuple]:
        return self.cursor.execute(f'SELECT * FROM {DEPARTURES};').fetchall()

    def getCurrentArrivals(self, current_time:int) -> list[tuple]:
        if isinstance(current_time, int): 
            return self.cursor.execute(f'SELECT * FROM {ARRIVALS} WHERE time >= ?', (current_time, )).fetchall()

    def getCurrentDepartures(self, current_time:int) -> list[tuple]:
        if isinstance(current_time, int): 
            return self.cursor.execute(f'SELECT * FROM {DEPARTURES} WHERE time >= ?', (current_time, )).fetchall()

    def deleteFlight(self, tablename:str, flight_code:tuple) -> None:
        self.cursor.execute(f'DELETE FROM {tablename} WHERE condition = "?"', flight_code) 
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
    def isValidDate(year:int, month:int, day:int) -> bool:
        try:
            datetime(year, month, day)
            return True
        except ValueError:
            print(f'The given date: {year}-{month}-{day} is invalid')
            return False

    def isValidFlightCode(airline:str, flight_code:str) -> bool:
        result = consultairlineflightcode(airline) 
        if not result:
           sys.stderr.write('No codes where found for the specified airline\n') 
           exit(1)
        if flight_code[:2] not in result:
            return False
        return True

    def confirmation(dataname:str, data):
        confirmation = input(f'Is this correct?\n{dataname} -> {user_input}\nInsert Y or N: ')
        return confirmation

    def getGeneralInput(message:str, valid_options:tuple, dataname:str):
        user_input = input(message)
        confirmation = confirmation(dataname, user_input)
        while user_input not in valid_options or confirmation != 'Y':
            user_input = input(f'You need to choose between {valid_options}: ')
            confirmation = confirmation(dataname, user_input)
        return user_input

    def getFlightCode(airline:str):
        flight_code = input('Insert flight code (minimum of 5 characters and maximum of 6 characters): ')
        confirmation = confirmation('flight_code', flight_code)
        is_valid_flight_code = isValidFlightCode(airline, flight_code)
        while (len(flight_code) != 5 and len(flight_code) != 6) or confirmation != 'Y' or not is_valid_flight_code:
            flight_code = input('Insert flight code (minimum of 5 characters and maximum of 6 characters): ')
            confirmation = confirmation('flight_code', flight_code)
            is_valid_flight_code = isValidFlightCode(airline, flight_code)
        return flight_code

    def getFlightTime():
        flight_date_time = input('Insert flight date time in the format of YYYY-MM-DD HH:MM: ')
        confirmation = confirmation('flight_date_time', flight_date_time)
        date = flight_date_time.split()[0].split('-')
        is_valid_date = isValidDate(date[0], date[1], date[2])
        while not re.search('^[0-9]{4}-(0[0-9]|[1][0-2])-([0-2][0-9]|3[0-1]) ([0-1][0-9]|[2][0-4]):[0-5][0-9]$') or confirmation != 'Y' \
                or not is_valid_date:
            flight_date_time = input('Insert flight date time in the format of YYYY-MM-DD HH:MM: ')
            confirmation = confirmation('flight_date_time', flight_date_time)
            date = flight_date_time.split()[0].split('-')
            is_valid_date = isValidDate(date[0], date[1], date[2])

        flight_date_time_object = datetime.strptime(flight_date_time, '%Y-%m-%d %H:%M')
        flight_date_time_epoch = int(flight_date_time_object.timestamp())
        return flight_date_time_epoch

    def getGate():
        flight_gate = input('Insert flight gate: ')
        confirmation = confirmation('flight gate', flight_gate)
        while confirmation != 'Y':
            flight_gate = input('Insert flight gate: ')
            confirmation = confirmation('flight gate', flight_gate)
        return flight_gate

    def getAirline():
        airline = input('Insert airline: ')
        confirmation = confirmation('airline', airline)
        while confirmation != 'Y':
            airline = input('Insert airline: ')
            confirmation = confirmation('airline', airline)
        return airline 

    def getOrigin():
        origin = input('Insert origin: ')
        confirmation = confirmation('Origin', origin)
        while confirmation != 'Y':
            origin = input('Insert origin: ')
            confirmation = confirmation('Origin', origin)
        return origin

    def getDestination():
        destination = input('Insert destination: ')
        confirmation = confirmation('destination', destination)
        while confirmation != 'Y':
            destination = input('Insert destination: ')
            confirmation = confirmation('destination', destination)
        return destination

    # Global variables
    database_file = 'test_flights.db'
    random_data_json_file = './random_data.json'

    flight_manager = FlightsManager(database_file)
    menu = '1) Update flight status\n2) Insert new flight\n3) Delete a flight\n4) Display flights\n5) Exit\n'
    print(menu)
    user_option = input('')
    while user_option != '5':
        if user_option == '1':
            # update flight status
            status = getGeneralInput(message='Insert flight status',\
                    valid_options=('on-time', 'delayed', 'cancelled'), dataname='status')
        elif user_option == '2':
            # insert flight
            tablename = getGeneralInput(message='Do you want to update a flight from arrivals or departures?: ',\
                    valid_options=(ARRIVALS, DEPARTURES), dataname='tablename')
            time = getFlightTime()
            gate = getGate()
            status = getGeneralInput(message='Insert flight status',\
                    valid_options=('on-time', 'delayed', 'cancelled'), dataname='status')
            airline = getAirline()
            flight_code = getFlightCode(airline)
            if tablename == ARRIVALS:
                origin = getOrigin()
            elif tablename == DEPARTURES:
                destination = getDestination()
        elif user_option == '3':
            # delete flight
            pass
        elif user_option == '4':
            # show flights
            pass
        else:
            sys.stderr.write(f'Unrecognized option: {user_option}\n')
            exit(1)
        print(menu)
        user_option = input('')

if __name__ == '__main__':
    main()
