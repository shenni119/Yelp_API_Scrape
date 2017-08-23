from yelp_key.py import *

import argparse
import json
import pprint
import requests
import sys
import urllib

# try:
#     from urllib.error import HTTPError
#     from urllib.parse import quote
#     from urllib.parse import urlencode
#
# API_HOST = 'https://api.yelp.com'
# SEARCH_PATH = '/v3/businesses/search'
# BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.
# TOKEN_PATH = '/oauth2/token'
# GRANT_TYPE = 'client_credentials'
#
#
# def obtain_bearer_token(host, path):
#     url = '{0}{1}'.format(host, quote(path.encode('utf8')))
#     data = urlencode({
#         'client_id': CLIENT_ID,
#         'client_secret': CLIENT_SECRET,
#         'grant_type': GRANT_TYPE,
#     })
#     response = requests.request('POST', url, data=data)
#     bearer_token = response.json()['access_token']
#     return bearer_token

import re

def request(host, path, bearer_token, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }
    print(u'Querying {0} ...'.format(url))
    response = requests.request('GET', url, headers=headers, params=url_params)
    return response.json()

LOCATION_CT = '02111'
LOCATION2 = '02116'
SEARCH_LIMIT = 50
OFFSET_COUNT=0
query_length=1000 #there aren't 1000 businesses in 02111, and this will capture all the businesses in 02116 as well.
loop_num=int(query_length/SEARCH_LIMIT)

outfile2 = open("{}_{}_businesses.txt".format(LOCATION_CT,LOCATION2),"w")

def search(bearer_token, location,offset_int):
    url_params = {
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT,
        'offset': offset_int
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)

yelp_response_list=[]
for query in range(loop_num):
    OFFSET_COUNT=query*SEARCH_LIMIT
    response=search(bearer_token2,LOCATION_CT,OFFSET_COUNT)
    yelp_response_list.append(json.dumps(response))

# print (str(yelp_response_list))
outfile2.write(str(yelp_response_list))
outfile2.close()

outfile3 = open("02111_02116_1000busi_url.csv","w")
outfile3.write("name,phone,business_url\n")

cachefile = open("{}_{}_businesses.txt".format(LOCATION_CT,LOCATION2),'r')
reading_cache=cachefile.read()

cache_list=ast.literal_eval(reading_cache)

for response in cache_list:
    python_obj=json.loads(response)
    for business in python_obj['businesses']:
        if business['location']['zip_code']=="02111" or business['location']['zip_code']=="02116":
            busi_name=business['name'].encode('utf8')
            busi_phone=business['display_phone']
            temp_url=business['url']
            busi_url=temp_url.split('?', 1)[0]
            outfile3.write("{},{},{}\n".format(busi_name,busi_phone,busi_url))
outfile3.close()
