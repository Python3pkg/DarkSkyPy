# -*- coding: utf-8 -*-
"""
recieves the api key and configures to build the request url.
"""

import sys
import os
import json
import requests
from attrdict import Attrdict

#Double check the naming convention for module,class,func stuff
class darksky(object):

    base_url = 'https://api.darksky.net/forecast/'


#TODO
#Need to add error catching for bad latlng or missing variables
    def __init__(self, location, **kwargs):
    #the api_key should be stored as an os.environment
    #instead of directly in the code
        API_KEY = os.environ.get('DARKSKY_API_KEY')

        self.latitude = location[0]
        self.longitude = location[1]
        self.api_key = API_KEY if API_KEY else kwargs.get('key', None)
    #follow the formatting in https://darksky.net/dev/docs/forecast
        self.params = {
            'exclude': kwargs.get('exclude', None),
            'extend': kwargs.get('extend', None),
            'lang': kwargs.get('lang', 'en'),
            'units': Kwargs.get('units', 'auto'),
        }
        if self.api_key is None:
            raise KeyError('Missing API Key')

        self.get_forecast(
            base_url,
            apikey=self.api_key
            latitude=self.latitude,
            longitude=self.longitude,
            params=self.params
        )

    def get_forecast(self, base_url, **kwargs):
        reply = _connect(base_url, **kwargs)
        jsonforecast = json.loads(reply)

        self.forecast = Attrdict(jsonforecast)    

    def _connect(self, base_url, **kwargs):
        """
        This function recieves the request url and it is used internaly to get
        the information via http.
        Returns the response content.
        Raises Timeout, TooManyRedirects, RequestException.
        Raises KeyError if headers are not present.
        Raises HTTPError if responde code is not 200.
        """
        url = base_url + '{apikey}/{latitude},{longitude}'.format(**kwargs)

        headers = {'Accept-Encoding': 'gzip, deflate'}
        try:
            r = requests.get(url, headers=headers, params=self.params, timeout=60)
            self.url = r.url

        except requests.exceptions.Timeout:
            print('Error: Timeout')
        except requests.exceptions.TooManyRedirects:
            print('Error: TooManyRedirects')
        except requests.exceptions.RequestException as ex:
            print(ex)
            sys.exit(1)

        # Response Headers see https://darksky.net/dev/docs/response
        try:
            self.cache_control = r.headers['Cache-Control']
            self.x_forecast_api_calls = r.headers['X-Forecast-API-Calls']
            self.x_responde_time = r.headers['X-Response-Time']
        except KeyError as kerr:
            print('Warning: Could not get headers.{0}').format(kerr)

        if r.status_code is not 200:
            raise requests.exceptions.HTTPError('Bad response')

        self.raw_response = r.text
        return self.raw_response
