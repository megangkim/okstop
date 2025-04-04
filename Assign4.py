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
from Flight import *
from Airport import *
from MaintenanceRecord import *

# Global containers
all_airports = []
all_flights = {}
maintenance_records = []

def load_flight_files(airport_file, flight_file):
    global all_airports, all_flights
    try:
        # Process airports file
        with open(airport_file, "r") as a_file:
            for record in a_file:
                rec = record.strip()
                if not rec:
                    continue
                elements = [elem.strip() for elem in rec.split('-') if elem.strip()]
                if len(elements) != 3:
                    continue  # ignore malformed lines
                airport_code, nation, municipality = elements[0], elements[1], elements[2]
                airport_obj = Airport(nation, municipality, airport_code)
                all_airports.append(airport_obj)
        # Process flights file
        with open(flight_file, "r") as f_file:
            for entry in f_file:
                text = entry.strip()
                if text == "":
                    continue
                tokens = [token.strip() for token in text.split('-') if token.strip()]
                if len(tokens) < 4:
                    continue
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
                origin_airport = None
                destination_airport = None
                for apt in all_airports:
                    if apt.get_code() == orig_code:
                        origin_airport = apt
                    if apt.get_code() == dest_code:
                        destination_airport = apt
                if origin_airport is None or destination_airport is None:
                    continue
                new_flight = Flight(origin_airport, destination_airport, flight_num, flight_duration)
                key = origin_airport.get_code()
                if key in all_flights:
                    all_flights[key].append(new_flight)
                else:
                    all_flights[key] = [new_flight]
        return True
    except Exception as error:
        return False

def get_airport_using_code(code):
    for apt in all_airports:
        if apt.get_code() == code:
            return apt
    raise ValueError("No airport with the given code: " + code)

def find_all_flights_city(city):
    results = []
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_city() == city or flight.get_destination().get_city() == city:
                results.append(flight)
    return results

def find_all_flights_country(country):
    results = []
    for flight_list in all_flights.values():
        for flight in flight_list:
            if flight.get_origin().get_country() == country or flight.get_destination().get_country() == country:
                results.append(flight)
    return results

def has_flight_between(orig_airport, dest_airport):
    key = orig_airport.get_code()
    if key in all_flights:
        for flt in all_flights[key]:
            if flt.get_destination() == dest_airport:
                return True
    return False

def shortest_flight_from(orig_airport):
    key = orig_airport.get_code()
    if key in all_flights and all_flights[key]:
        candidate = all_flights[key][0]
        for flt in all_flights[key]:
            if flt.get_duration() < candidate.get_duration():
                candidate = flt
        return candidate
    return None

def find_return_flight(flight):
    start = flight.get_origin()
    end = flight.get_destination()
    key = end.get_code()
    if key in all_flights:
        for ret_flight in all_flights[key]:
            if ret_flight.get_destination() == start:
                return ret_flight
    raise ValueError("There is no flight from " + end.get_code() + " to " + start.get_code())

def create_maintenance_records(maintenance_file, flights_dict, airports_list):
    global maintenance_records
    try:
        with open(maintenance_file, "r") as m_file:
            for line in m_file:
                clean_line = line.strip()
                if not clean_line:
                    continue
                try:
                    record_instance = MaintenanceRecord(clean_line, flights_dict, airports_list)
                    if not any(record_instance == exist_rec for exist_rec in maintenance_records):
                        maintenance_records.append(record_instance)
                except ValueError:
                    return False
        return True
    except Exception:
        return False

def find_total_cost(records):
    cost_sum = 0
    for rec in records:
        cost_sum += rec.get_total_cost()
    return cost_sum

def find_total_duration(records):
    duration_sum = 0
    for rec in records:
        duration_sum += rec.get_duration()
    return duration_sum

def sort_maintenance_records(records):
    return sorted(records)

if __name__ == "__main__":
    pass
