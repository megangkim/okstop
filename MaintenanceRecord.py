"""
*************************************************
CS 1026B Assignment 4 – Air Travel
Code by: Megan Kim
Student ID: 251431752
File created: April 2, 2025
Description: Contains the MaintenanceRecord class that encapsulates maintenance details for flights.
*************************************************
"""
import re  # Regular expressions will help validate the flight number format
from Flight import *  # Bring in the Flight class so we can use existing flight data
from Airport import *  # We'll need to match airports too

class MaintenanceRecord:
    def __init__(self, input_line, all_flights, all_airports):
        # Clean up the string from any random spacing
        cleaned_line = input_line.strip()

        # Break the string into parts, separated by hyphens (e.g., "ABC-123-YYZ-2-100")
        parts = [piece.strip() for piece in cleaned_line.split('-') if piece.strip()]

        # Depending on how the flight number is formatted, grab the right pieces
        if len(parts) == 5:
            # If it's split into 5 (like 'ABC' + '123'), join first two to get full flight number
            flight_number = parts[0] + '-' + parts[1]
            maint_airport_code = parts[2]
            duration_str = parts[3]
            cost_str = parts[4]
        elif len(parts) == 4:
            # Already joined flight number (e.g., 'ABC-123')
            flight_number, maint_airport_code, duration_str, cost_str = parts
        else:
            # If it's neither 4 nor 5 parts, then something’s wrong with the format
            raise ValueError("Invalid data string")

        # Check if the flight number looks like something valid (e.g., "ABC-123")
        if not re.match(r"^[A-Z]{3}-\d{3}$", flight_number):
            raise ValueError("Invalid data string")

        # Try turning the duration and cost into numbers — must be numeric
        try:
            maintenance_duration = float(duration_str)
            maintenance_cost_per_hour = float(cost_str)
        except Exception:
            # Something went wrong with converting to float
            raise ValueError("Invalid data string")

        # Now find the Flight object that matches the flight number
        found_flight = None
        for flight_list in all_flights.values():
            for flight in flight_list:
                if flight.get_number() == flight_number:
                    found_flight = flight
                    break
            if found_flight:
                break  # Once we’ve found it, no need to keep looking

        # If we couldn't find a match, we can’t continue
        if found_flight is None:
            raise ValueError("Flight not found")

        # Same deal, but for the maintenance airport — match by code
        found_airport = None
        for airport in all_airports:
            if airport.get_code() == maint_airport_code:
                found_airport = airport
                break

        # Again, raise an error if the airport doesn’t exist
        if found_airport is None:
            raise ValueError("Airport not found")

        # Save all the final pieces as private variables in the object
        self._flight = found_flight
        self._maintenance_airport = found_airport
        self._maintenance_duration = maintenance_duration
        self._maintenance_cost_per_hour = maintenance_cost_per_hour

    # Calculate the full cost for maintenance (time × cost per hour)
    def get_total_cost(self):
        return self._maintenance_duration * self._maintenance_cost_per_hour

    # Just return how long the maintenance takes
    def get_duration(self):
        return self._maintenance_duration

    # When printing the object, show all the important details in one line
    def __str__(self):
        flight_str = f"{self._flight.get_number()} ({self._flight})"
        origin_str = f"{self._flight.get_origin()}"
        maint_airport_str = f"{self._maintenance_airport}"
        total_cost = self.get_total_cost()

        return (f"{flight_str} from {origin_str} to be maintained at {maint_airport_str} "
                f"for {int(self._maintenance_duration)} hours @ ${self._maintenance_cost_per_hour}/hour "
                f"(${total_cost})")

    # Check if two maintenance records are the same (same flight, airport, hours, and rate)
    def __eq__(self, other):
        if not isinstance(other, MaintenanceRecord):
            return False
        return (self._flight == other._flight and
                self._maintenance_airport == other._maintenance_airport and
                self._maintenance_duration == other._maintenance_duration and
                self._maintenance_cost_per_hour == other._maintenance_cost_per_hour)

    # Define "not equal" just as the opposite of equal
    def __ne__(self, other):
        return not self.__eq__(other)

    # Use total cost to compare which record is "less than" another
    def __lt__(self, other):
        return self.get_total_cost() < other.get_total_cost()

    # Same, but for "less than or equal"
    def __le__(self, other):
        return self.get_total_cost() <= other.get_total_cost()

    # Greater than = higher total maintenance cost
    def __gt__(self, other):
        return self.get_total_cost() > other.get_total_cost()

    # Greater than or equal = same idea, just inclusive
    def __ge__(self, other):
        return self.get_total_cost() >= other.get_total_cost()

