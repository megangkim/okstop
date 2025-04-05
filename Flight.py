"""
******************************
CS 1026B Assignment 4 – Air Travel
Code by: Megan Kim
Student ID: 251431752
File created: April 4, 2025
Description: This file defines the Flight class used to represent a flight between two airports.
******************************
"""
from Airport import *  # We need to use the Airport class for origin and destination airports

class Flight:
    def __init__(self, origin, destination, flight_number, duration):
        # Just making sure we’re passing in actual Airport objects
        if not (isinstance(origin, Airport) and isinstance(destination, Airport)):
            raise TypeError("The origin and destination must be Airport objects")

        self._origin = origin                            # Save where the flight starts
        self._destination = destination                  # Save where the flight ends
        self._flight_number = flight_number              # Unique flight code like "ABC-123"
        self._duration = float(duration)                 # Duration in hours (as float just in case decimals are needed)

    def __str__(self):
        # Show if it’s a domestic or international flight (same country or not)
        domestic_str = "domestic" if self.is_domestic() else "international"
        return f"{self._origin.get_city()} to {self._destination.get_city()} ({domestic_str}) [{round(self._duration)}h]"

    def __eq__(self, other):
        # Two flights are considered the same if they go between the same airports
        if not isinstance(other, Flight):
            return False
        return (self._origin == other._origin) and (self._destination == other._destination)

    def __add__(self, conn_flight):
        # Combine two flights into one (like connecting flights), if the destination of the first
        # is the same as the origin of the second
        if not isinstance(conn_flight, Flight):
            raise TypeError("The connecting_flight must be a Flight object")
        if self._destination != conn_flight._origin:
            raise ValueError("These flights cannot be combined")

        new_duration = self._duration + conn_flight._duration
        # Return a new Flight object that goes from the first origin to the final destination
        return Flight(self._origin, conn_flight._destination, self._flight_number, new_duration)

    # Returns the flight number like "ABC-123"
    def get_number(self):
        return self._flight_number

    # Where the flight starts
    def get_origin(self):
        return self._origin

    # Where the flight lands
    def get_destination(self):
        return self._destination

    # How long the flight takes in hours
    def get_duration(self):
        return self._duration

    # Checks if both airports are in the same country
    def is_domestic(self):
        return self._origin.get_country() == self._destination.get_country()

    # Let you change the origin airport if needed
    def set_origin(self, origin):
        self._origin = origin

    # Let you change the destination airport
    def set_destination(self, destination):
        self._destination = destination

