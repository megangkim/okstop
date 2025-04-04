"""
*************************************************
CS 1026B Assignment 4 – Air Travel
Code by: Megan Kim
Student ID: 251431752
File created: April 2, 2025
Description: Contains the MaintenanceRecord class that encapsulates maintenance details for flights.
*************************************************
"""
import re                          # Import regular expressions for pattern checking
from Flight import *              # Import the Flight class
from Airport import *             # Import the Airport class

class MaintenanceRecord:
    def __init__(self, input_line, all_flights, all_airports):
        # Clean and split the input data
        cleaned_line = input_line.strip()
        parts = [piece.strip() for piece in cleaned_line.split('-') if piece.strip()]

        # Extract values depending on number of tokens (4 or 5 parts)
        if len(parts) == 5:
            flight_number = parts[0] + '-' + parts[1]
            maint_airport_code = parts[2]
            duration_str = parts[3]
            cost_str = parts[4]
        elif len(parts) == 4:
            flight_number, maint_airport_code, duration_str, cost_str = parts
        else:
            raise ValueError("Invalid data string")  # Raise error for incorrect format

        # Check that the flight number matches format "AAA-000"
        if not re.match(r"^[A-Z]{3}-\d{3}$", flight_number):
            raise ValueError("Invalid data string")

        # Convert duration and cost to floats
        try:
            maintenance_duration = float(duration_str)
            maintenance_cost_per_hour = float(cost_str)
        except Exception:
            raise ValueError("Invalid data string")

        # Look for the matching Flight object
        found_flight = None
        for flight_list in all_flights.values():
            for flight in flight_list:
                if flight.get_number() == flight_number:
                    found_flight = flight
                    break
            if found_flight:
                break

        if found_flight is None:
            raise ValueError("Flight not found")  # No matching flight found

        # Look for the matching Airport object
        found_airport = None
        for airport in all_airports:
            if airport.get_code() == maint_airport_code:
                found_airport = airport
                break

        if found_airport is None:
            raise ValueError("Airport not found")  # No matching airport found

        # Store attributes
        self._flight = found_flight
        self._maintenance_airport = found_airport
        self._maintenance_duration = maintenance_duration
        self._maintenance_cost_per_hour = maintenance_cost_per_hour

    # Calculate and return total cost = duration × cost/hour
    def get_total_cost(self):
        return self._maintenance_duration * self._maintenance_cost_per_hour

    # Return the maintenance duration
    def get_duration(self):
        return self._maintenance_duration

    # Define how the object is printed
    def __str__(self):
        flight_str = f"{self._flight.get_number()} ({self._flight})"
        origin_str = f"{self._flight.get_origin()}"
        maint_airport_str = f"{self._maintenance_airport}"
        total_cost = self.get_total_cost()
        return (f"{flight_str} from {origin_str} to be maintained at {maint_airport_str} "
                f"for {int(self._maintenance_duration)} hours @ ${self._maintenance_cost_per_hour}/hour "
                f"(${total_cost})")

    # Check if two maintenance records are equal (same flight, airport, duration, cost)
    def __eq__(self, other):
        if not isinstance(other, MaintenanceRecord):
            return False
        return (self._flight == other._flight and
                self._maintenance_airport == other._maintenance_airport and
                self._maintenance_duration == other._maintenance_duration and
                self._maintenance_cost_per_hour == other._maintenance_cost_per_hour)

    # Check if two records are NOT equal
    def __ne__(self, other):
        return not self.__eq__(other)

    # Less than comparison based on total cost
    def __lt__(self, other):
        return self.get_total_cost() < other.get_total_cost()

    # Less than or equal to comparison
    def __le__(self, other):
        return self.get_total_cost() <= other.get_total_cost()

    # Greater than comparison
    def __gt__(self, other):
        return self.get_total_cost() > other.get_total_cost()

    # Greater than or equal to comparison
    def __ge__(self, other):
        return self.get_total_cost() >= other.get_total_cost()
