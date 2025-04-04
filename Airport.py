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
        self._country = country
        self._city = city
        self._code = code

    def __str__(self):
        return f"{self._code} [{self._city}, {self._country}]"

    def __eq__(self, other):
        if not isinstance(other, Airport):
            return False
        return self._code == other._code

    def get_code(self):
        return self._code

    def get_city(self):
        return self._city

    def get_country(self):
        return self._country

    def set_city(self, city):
        self._city = city

    def set_country(self, country):
        self._country = country
