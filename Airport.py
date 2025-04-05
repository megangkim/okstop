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
    def __init__(self, country, city, code):
        # Save the basic details of the airport
        self._country = country     # Country the airport is located in
        self._city = city           # City the airport is in
        self._code = code           # 3-letter airport code (e.g., YYZ or LAX)

    def __str__(self):
        # When we print the airport, this is how it will look
        return f"{self._code} [{self._city}, {self._country}]"

    def __eq__(self, other):
        # Airports are considered equal if their codes match
        if not isinstance(other, Airport):
            return False
        return self._code == other._code

    # Just returns the airport code (used a lot in comparisons and keys)
    def get_code(self):
        return self._code

    # Returns the city name
    def get_city(self):
        return self._city

    # Returns the country name
    def get_country(self):
        return self._country

    # Lets us update the city name if needed
    def set_city(self, city):
        self._city = city

    # Lets us update the country name if needed
    def set_country(self, country):
        self._country = country
