# Airport Flight timetable

**This project is currently under development.**

This project simulates an airport flight information screen, allowing users to view flights and workers to manage the database.

## Features
- **Display Flights**: A terminal-based program to display flight details. This program automatically updates and only shows flights that have a departure time greater than or equal to the current time.(`displayflights.py`).
- **Manage Database**: Tools to manage the flight database (`managedatabase.py`).
- **Test Mode**: Populate the database with random data for a demo experience (`generaterandomdata.py`).
- **Loading Animations**: Terminal animations during operations (`loadingmotions.py`).

## Modules
1. **`displayflights.py`**: Displays the flight details in a terminal interface.
2. **`managedatabase.py`**: Manages flight data in the database.
3. **`generaterandomdata.py`**: Generates random flight data when test mode is activated.
4. **`loadingmotions.py`**: Provides animations for terminal progress bars or loading screens.
5. **consultairlineflightcode.py**: Consult IATA to check the two-letter code associated with a specific airline.

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
#### Normal Mode
Run the program to display flights:
```bash
python displayflights.py
```

#### Test Mode
Run the program with the `--test` option to populate the database with random data for demo purposes:
```bash
python managedatabase.py --test
```
