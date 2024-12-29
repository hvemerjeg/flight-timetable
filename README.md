# Airport Flight timetable
This simple project simulates an airport flight information screen, allowing users to view flights and workers to manage the database.

## Features
- **Display Flights**: A terminal-based program to display flight details. This program automatically updates and only shows flights within the next 24 hours.(`displayflights.py`).
- **Manage Database**: Tools to manage the flight database (`managedatabase.py`). This is for the workers to manage the flights information manually when needed.

## Modules
1. **`displayflights.py`**: Displays the flight details in a terminal interface.
2. **`managedatabase.py`**: Manages flight data in the database.
3. **`generaterandomdata.py`**: Generates random flight data when test mode is activated.
4. **`loadingmotions.py`**: Provides animations for terminal progress bars or loading screens.
5. **`consultairlineflightcode.py`**: Consult IATA to check the two-letter code associated with a specific airline.
6. **`formattime.py`**: To format date and time.
7. **`cleaninput.py`**: To clean the user input.

## Getting Started

### Prerequisites
- Python 3.x

### Installation
1. Clone this repository:  
   ```bash
   git clone https://github.com/hvemerjeg/flight-timetable.git
   cd flight-timetable 
   ```
### Usage
#### Get help
List the available options:
```bash
python displayflights.py --help
python managedatabase.py --help
```
#### Normal Mode
Run the program to display flights:
```bash
python displayflights.py
```

Run the program to manage flights information:
```bash
python managedatabase.py
```

#### Test Mode
Run the program with the `--test` option to populate the database with random data for demo purposes:
```bash
python displayflights.py --test
python managedatabase.py --test
```
