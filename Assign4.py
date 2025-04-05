"""
**********************************************************
CS 1026B Assignment 4 – Air Travel
Code by: Megan Kim
Student ID: 251431752
File created: April 4, 2025
Description: Main module for processing air travel data. It reads from text files,
instantiates Airport, Flight, and MaintenanceRecord objects, and provides analysis functions.
**********************************************************
"""
from Flight import *                # Brings in the Flight class
from Airport import *               # Brings in the Airport class
from MaintenanceRecord import *     # Imports the MaintenanceRecord class

# These will store everything we load from the input files
all_airports = []         # List of Airport objects
all_flights = {}          # Maps airport codes to a list of outbound flights
maintenance_records = []  # List of all maintenance jobs

# Reads airport and flight data from input files and builds the main lists/dictionaries
def load_flight_files(airport_file, flight_file):
    global all_airports, all_flights
    try:
        # First: read and build Airport objects
        with open(airport_file, "r") as a_file:
            for record in a_file:
                rec = record.strip()
                if not rec:
                    continue  # Ignore any empty lines
                elements = [elem.strip() for elem in rec.split('-') if elem.strip()]
                if len(elements) != 3:
                    continue  # We only accept well-formed records with 3 parts
                airport_code, nation, municipality = elements[0], elements[1], elements[2]
                airport_obj = Airport(nation, municipality, airport_code)
                all_airports.append(airport_obj)

        # Second: load the flight data and attach to corresponding airports
        with open(flight_file, "r") as f_file:
            for entry in f_file:
                text = entry.strip()
                if text == "":
                    continue  # Skip blank lines
                tokens = [token.strip() for token in text.split('-') if token.strip()]
                if len(tokens) < 4:
                    continue  # Flight record is too short to be useful

                # Depending on the format, either reconstruct or keep the flight number
                if len(tokens) >= 5:
                    flight_num = tokens[0] + '-' + tokens[1]
                    orig_code = tokens[2]
                    dest_code = tokens[3]
                    flight_duration = tokens[4]
                else:
                    flight_num = tokens[0]
                    orig_code = tokens[1]
                    dest_code = tokens[2]
                    flight_duration = tokens[3]

                # Match the origin and destination codes to actual Airport objects
                origin_airport = None
                destination_airport = None
                for apt in all_airports:
                    if apt.get_code() == orig_code:
                        origin_airport = apt
                    if apt.get_code() == dest_code:
                        destination_airport = apt

                if origin_airport is None or destination_airport is None:
                    continue  # Skip this flight if either airport wasn't found

                # Create the flight and store it under the origin's code
                new_flight = Flight(origin_airport, destination_airport, flight_num, flight_duration)
                key = origin_airport.get_code()
                if key in all_flights:
                    all_flights[key].append(new_flight)
                else:
                    all_flights[key] = [new_flight]
        return True
    except Exception as error:
        # If anything fails (file missing, bad format, etc.), return False
        return False

# Looks up an airport by its 3-letter code
def get_airport_using_code(code):
    for apt in all_airports:
        if apt.get_code() == code:
            return apt
    # Didn't find anything with that code
    raise ValueError("No airport with the given code: " + code)

# Returns every flight that starts or ends in the given city
def find_all_flights_city(city):
    results = []
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_city() == city or flight.get_destination().get_city() == city:
                results.append(flight)
    return results

# Returns every flight that starts or ends in the given country
def find_all_flights_country(country):
    results = []
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_country() == country or flight.get_destination().get_country() == country:
                results.append(flight)
    return results

# Checks if a flight exists from one airport to another
def has_flight_between(orig_airport, dest_airport):
    key = orig_airport.get_code()
    if key in all_flights:
        for flt in all_flights[key]:
            if flt.get_destination() == dest_airport:
                return True
    return False

# Finds the shortest (duration-wise) flight leaving from a given airport
def shortest_flight_from(orig_airport):
    key = orig_airport.get_code()
    if key in all_flights and all_flights[key]:
        candidate = all_flights[key][0]
        for flt in all_flights[key]:
            if flt.get_duration() < candidate.get_duration():
                candidate = flt
        return candidate
    return None  # No flights available from this airport

# Finds a return flight (opposite direction of the given flight)
def find_return_flight(flight):
    start = flight.get_origin()
    end = flight.get_destination()
    key = end.get_code()
    if key in all_flights:
        for ret_flight in all_flights[key]:
            if ret_flight.get_destination() == start:
                return ret_flight
    raise ValueError("There is no flight from " + end.get_code() + " to " + start.get_code())

# Reads the maintenance file and creates MaintenanceRecord objects from it
def create_maintenance_records(maintenance_file, flights_dict, airports_list):
    global maintenance_records
    try:
        with open(maintenance_file, "r") as m_file:
            for line in m_file:
                clean_line = line.strip()
                if not clean_line:
                    continue  # Skip blanks
                try:
                    record_instance = MaintenanceRecord(clean_line, flights_dict, airports_list)
                    # Avoid duplicate entries
                    if not any(record_instance == exist_rec for exist_rec in maintenance_records):
                        maintenance_records.append(record_instance)
                except ValueError:
                    return False  # If the line can't be parsed, we fail early
        return True
    except Exception:
        return False  # File couldn't be opened or parsed

# Adds up the total cost across all maintenance records
def find_total_cost(records):
    cost_sum = 0
    for rec in records:
        cost_sum += rec.get_total_cost()
    return cost_sum

# Adds up total duration (hours) of maintenance work
def find_total_duration(records):
    duration_sum = 0
    for rec in records:
        duration_sum += rec.get_duration()
    return duration_sum

# Returns a new sorted list of maintenance records (by total cost)
def sort_maintenance_records(records):
    return sorted(records)

# Doesn’t run anything unless the file is being run directly
if __name__ == "__main__":
    pass
