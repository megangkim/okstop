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
from Flight import *              # Import the Flight class
from Airport import *             # Import the Airport class
from MaintenanceRecord import *   # Import the MaintenanceRecord class

# Global containers to store data
all_airports = []         # List of all Airport objects
all_flights = {}          # Dictionary mapping airport codes to Flight lists
maintenance_records = []  # List of all MaintenanceRecord objects

# Loads airport and flight data from text files
def load_flight_files(airport_file, flight_file):
    global all_airports, all_flights
    try:
        # Open and read the airport file
        with open(airport_file, "r") as a_file:
            for record in a_file:
                rec = record.strip()
                if not rec:
                    continue  # Skip empty lines
                # Clean and split each record
                elements = [elem.strip() for elem in rec.split('-') if elem.strip()]
                if len(elements) != 3:
                    continue  # Skip malformed lines
                airport_code, nation, municipality = elements[0], elements[1], elements[2]
                airport_obj = Airport(nation, municipality, airport_code)
                all_airports.append(airport_obj)

        # Open and read the flights file
        with open(flight_file, "r") as f_file:
            for entry in f_file:
                text = entry.strip()
                if text == "":
                    continue
                tokens = [token.strip() for token in text.split('-') if token.strip()]
                if len(tokens) < 4:
                    continue  # Skip incomplete lines

                # Handle flight number formatting
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

                # Match origin and destination airports from list
                origin_airport = None
                destination_airport = None
                for apt in all_airports:
                    if apt.get_code() == orig_code:
                        origin_airport = apt
                    if apt.get_code() == dest_code:
                        destination_airport = apt

                if origin_airport is None or destination_airport is None:
                    continue  # Skip if airport code not found

                # Create Flight object and add it to the dictionary
                new_flight = Flight(origin_airport, destination_airport, flight_num, flight_duration)
                key = origin_airport.get_code()
                if key in all_flights:
                    all_flights[key].append(new_flight)
                else:
                    all_flights[key] = [new_flight]
        return True  # Loading successful
    except Exception as error:
        return False  # Loading failed

# Find and return an Airport object using its code
def get_airport_using_code(code):
    for apt in all_airports:
        if apt.get_code() == code:
            return apt
    raise ValueError("No airport with the given code: " + code)

# Return all flights that involve a given city
def find_all_flights_city(city):
    results = []
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_city() == city or flight.get_destination().get_city() == city:
                results.append(flight)
    return results

# Return all flights that involve a given country
def find_all_flights_country(country):
    results = []
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_country() == country or flight.get_destination().get_country() == country:
                results.append(flight)
    return results

# Check if a flight exists between two specific airports
def has_flight_between(orig_airport, dest_airport):
    key = orig_airport.get_code()
    if key in all_flights:
        for flt in all_flights[key]:
            if flt.get_destination() == dest_airport:
                return True
    return False

# Find and return the shortest flight from a given airport
def shortest_flight_from(orig_airport):
    key = orig_airport.get_code()
    if key in all_flights and all_flights[key]:
        candidate = all_flights[key][0]
        for flt in all_flights[key]:
            if flt.get_duration() < candidate.get_duration():
                candidate = flt
        return candidate
    return None  # No flights from the airport

# Look for a return flight that goes back to the origin
def find_return_flight(flight):
    start = flight.get_origin()
    end = flight.get_destination()
    key = end.get_code()
    if key in all_flights:
        for ret_flight in all_flights[key]:
            if ret_flight.get_destination() == start:
                return ret_flight
    raise ValueError("There is no flight from " + end.get_code() + " to " + start.get_code())

# Create maintenance record objects from a file and add to the list
def create_maintenance_records(maintenance_file, flights_dict, airports_list):
    global maintenance_records
    try:
        with open(maintenance_file, "r") as m_file:
            for line in m_file:
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    # Create a MaintenanceRecord and avoid duplicates
                    record_instance = MaintenanceRecord(clean_line, flights_dict, airports_list)
                    if not any(record_instance == exist_rec for exist_rec in maintenance_records):
                        maintenance_records.append(record_instance)
                except ValueError:
                    return False
        return True
    except Exception:
        return False

# Compute total cost of all maintenance records
def find_total_cost(records):
    cost_sum = 0
    for rec in records:
        cost_sum += rec.get_total_cost()
    return cost_sum

# Compute total duration of all maintenance records
def find_total_duration(records):
    duration_sum = 0
    for rec in records:
        duration_sum += rec.get_duration()
    return duration_sum

# Return a sorted list of maintenance records
def sort_maintenance_records(records):
    return sorted(records)

# Main guard to allow import without running
if __name__ == "__main__":
    pass
