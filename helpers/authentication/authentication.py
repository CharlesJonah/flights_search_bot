""" Handles Wolfnet API Authenication """
import os

from helpers.services import HttpService
from constants import AMADEUS_BASE_AUTHENTICATION_API


class Authenticate:
    """ Handle wolfnet API Authentication """

    def __init__(self):
        self.http_service = HttpService()

    def login(self):
        """ Log in by setting api_token header in the http_service object """
        res = self.http_service.post(AMADEUS_BASE_AUTHENTICATION_API, {
            'client_id': os.environ['AMADEUS_API_KEY'], 'client_secret': os.environ['AMADEUS_API_SECRET'],
            'grant_type':'client_credentials'})
        print(res.json())
        self.http_service.config_service(
            {'Authorization': f"Bearer {res.json()['access_token']}"})

    def logout(self):
        """ Log out by setting api_token header in the http_service object to None"""
        self.http_service.config_service(
            {'Authorization': None})