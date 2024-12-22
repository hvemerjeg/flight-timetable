import sqlite3
from os import path, system
import sys
from time import sleep
import random
import json
from datetime import datetime, timedelta
import re

# Constants
ARRIVALS = 'arrivals'
DEPARTURES = 'departures'

def takeUserInput(message:str, valid_options:tuple, dataname:str):
    user_input = input(message)
    confirmation = 'N'
    while user_input not in valid_options or confirmation != 'Y':
        user_input = input(f'You need to choose between {valid_options}: ')
        confirmation = input(f'Is this correct?\n{dataname} -> {user_input}\nInsert Y or N: ')
    return user_input

def getUserFlightCode():
    flight_code = input('Insert flight code (minimum of 5 characters and maximum of 6 characters): ')
    confirmation = input(f'Is this correct?\nflight_code -> {flight_code}\nInsert Y or N: ')
    while (len(flight_code) != 5 and len(flight_code) != 6) or confirmation != 'Y':
        flight_code = input('Insert flight code (minimum of 5 characters and maximum of 6 characters): ')
        confirmation = input(f'Is this correct?\nflight_code -> {flight_code}\nInsert Y or N: ')
    return flight_code

def getUserFlightTime():
    flight_time = input('Insert user flight time in the format of 23:00: ')
    confirmation = input(f'Is this correct?\nflight_time -> {flight_time}\nInsert Y or N: ')
    while not re.search('^([0-1][0-9]|[2][0-4]):[0-5][0-9]$') or confirmation != 'Y':
        flight_time = input('Insert user flight time in the format of 23:00: ')
        confirmation = input(f'Is this correct?\nflight_time -> {flight_time}\nInsert Y or N: ')
    return flight_time

class FlightsManager:
    def __init__(self, databasefile='./flights.db'):
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

    def getFlightTime(self, tablename:str, flight_code:str):
        if tablename == ARRIVALS or tablename == DEPARTURES:
            return self.cursor.execute(f'SELECT time FROM {tablename} WHERE flight_code = "?";', (flight_code)).fetchall()

    def getAllArrivals(self):
        return self.cursor.execute(f'SELECT * FROM {ARRIVALS};').fetchall()

    def getAllDepartures(self):
        return self.cursor.execute(f'SELECT * FROM {DEPARTURES};').fetchall()

    def getCurrentArrivals(self, current_time:int):
        if isinstance(current_time, int): 
            return self.cursor.execute(f'SELECT * FROM {ARRIVALS} WHERE time >= ?', (current_time, )).fetchall()

    def getCurrentDepartures(self, current_time:int):
        if isinstance(current_time, int): 
            return self.cursor.execute(f'SELECT * FROM {DEPARTURES} WHERE time >= ?', (current_time, )).fetchall()

    def deleteFlight(self, tablename:str, flight_code:tuple):
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
    # Global variables
    database_file = 'flights.db'
    random_data_json_file = './random_data.json'

    flight_manager = FlightsManager(database_file)
    menu = '1) Update flight status\n2) Insert new flight\n3) Delete a flight\n4) Display flights\n5) Exit\n'
    print(menu)
    user_option = input('')
    while user_option != '5':
        if user_option == '1':
            # update flight status
            tablename = takeUserInput(message='Do you want to update a flight from arrivals or departures?: ',\
                    valid_options=(ARRIVALS, DEPARTURES), dataname='tablename')
            flight_code = getUserFlightCode()
            time = getUserFlightTime()
            if tablename == ARRIVALS:
                pass
            elif tablename == DEPARTURES:
                pass

        elif user_option == '2':
            # insert flight
            pass
        elif user_option == '3':
            # delete flight
            pass
        elif user_option == '4':
            # show flights
            sleep(1)
            flight_manager.showFlights() 
        else:
            sys.stderr.write(f'Unrecognized option: {user_option}\n')
            exit(1)
        print(menu)
        user_option = input('')

if __name__ == '__main__':
    main()
