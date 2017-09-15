#!/usr/bin/env python
# -*-coding: utf-8 -*-

import shodan
import requests

SHODAN_API_KEY = "SlFqdFrz7t2Gw2Dbh4wGlOUDg6sAiOBK"
api = shodan.Shodan(SHODAN_API_KEY)

try:
        # Search Shodan
        results = api.search('joomla')

        # Show the results
        print 'Results found: %s' % results['total']
        for result in results['matches']:
                print 'http://' + result['ip_str']
except shodan.APIError, e:
        print 'Error: %s' % e
