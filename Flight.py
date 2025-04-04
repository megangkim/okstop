"""
******************************
CS 1026B Assignment 4 – Air Travel
Code by: Megan Kim
Student ID: 251431752
File created: April 4, 2025
Description: This file defines the Flight class used to represent a flight between two airports.
******************************
"""
from Airport import *  # Import the Airport class to use for origin and destination

class Flight:
    # Constructor method to initialize a Flight object
    def __init__(self, origin, destination, flight_number, duration):
        # Ensure origin and destination are Airport objects
        if not (isinstance(origin, Airport) and isinstance(destination, Airport)):
            raise TypeError("The origin and destination must be Airport objects")
        self._origin = origin                      # Store the origin airport
        self._destination = destination            # Store the destination airport
        self._flight_number = flight_number        # Store the flight number as a string
        self._duration = float(duration)           # Store the flight duration as a float

    # Define how the flight is displayed as a string
    def __str__(self):
        # Add "domestic" or "international" label based on countries
        domestic_str = "domestic" if self.is_domestic() else "international"
        return f"{self._origin.get_city()} to {self._destination.get_city()} ({domestic_str}) [{round(self._duration)}h]"

    # Define equality between two Flight objects based on origin and destination
    def __eq__(self, other):
        if not isinstance(other, Flight):  # Ensure the other object is a Flight
            return False
        return (self._origin == other._origin) and (self._destination == other._destination)

    # Define how two flights can be added (combined into a new flight)
    def __add__(self, conn_flight):
        # Ensure the other flight is a Flight object
        if not isinstance(conn_flight, Flight):
            raise TypeError("The connecting_flight must be a Flight object")
        # The destination of the first must match the origin of the second
        if self._destination != conn_flight._origin:
            raise ValueError("These flights cannot be combined")
        # Combine durations, keep same flight number
        new_duration = self._duration + conn_flight._duration
        return Flight(self._origin, conn_flight._destination, self._flight_number, new_duration)

    # Getter for the flight number
    def get_number(self):
        return self._flight_number

    # Getter for the origin airport
    def get_origin(self):
        return self._origin

    # Getter for the destination airport
    def get_destination(self):
        return self._destination

    # Getter for the duration
    def get_duration(self):
        return self._duration

    # Check if the flight is domestic (same country for origin and destination)
    def is_domestic(self):
        return self._origin.get_country() == self._destination.get_country()

    # Setter to change the origin airport
    def set_origin(self, origin):
        self._origin = origin

    # Setter to change the destination airport
    def set_destination(self, destination):
        self._destination = destination
