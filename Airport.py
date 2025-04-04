"""
******************************
CS 1026B Assignment 4 – Air Travel
Code by: Megan Kim
Student ID: 251431752
File created: April 4, 2025
Description: This file defines the Airport class used to represent an airport.
******************************
"""

class Airport:
    # Constructor method to initialize the airport's country, city, and code
    def __init__(self, country, city, code):
        self._country = country  # Store the country name
        self._city = city        # Store the city name
        self._code = code        # Store the airport code (e.g., "YYZ")

    # Define how the airport object is printed as a string
    def __str__(self):
        return f"{self._code} [{self._city}, {self._country}]"

    # Define equality check between two Airport objects
    def __eq__(self, other):
        if not isinstance(other, Airport):  # Check if 'other' is an Airport object
            return False
        return self._code == other._code    # Airports are equal if their codes match

    # Getter method for the airport code
    def get_code(self):
        return self._code

    # Getter method for the city name
    def get_city(self):
        return self._city

    # Getter method for the country name
    def get_country(self):
        return self._country

    # Setter method to update the city name
    def set_city(self, city):
        self._city = city

    # Setter method to update the country name
    def set_country(self, country):
        self._country = country
