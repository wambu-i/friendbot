import json
import os

import logging
import requests
import sys

from urllib.parse import urlparse, urljoin

formatter = '[%(asctime)-15s] %(levelname)s [%(filename)s.%(funcName)s#L%(lineno)d] - %(message)s'

logging.basicConfig(level = logging.DEBUG, format = formatter)

app_id = os.environ.get('ID', None)
app_secret = os.environ.get('SECRET', None)
access_token = os.environ.get('UAT', None)

# Create logger instance
logger = logging.getLogger('api')
graph = "https://graph.facebook.com/v3.3/{0}?fields=id,name,fan_count&access_token={1}"

def create_new_page(token):
    #Creates a new page
    pass

def query_page_id(name):
    headers = {
        'Content-Type' : 'application/json'
    }

    r = requests.get(graph.format(name, access_token))
    page = r.json()
    return page["id"]

def get_page_id(url):
    id = None
    page = urlparse(url).path
    if page:
        id = page.rsplit('-')
        if len(id) > 1:
            id = id[-1].strip('/')
        else:
            name = id[0].strip('/')
            id = query_page_id(name)
    
    return id

def exchangeTokens(app_id, app_secret, access_token):
	base_url = 'https://graph.facebook.com/v3.3/oauth/access_token?grant_type=fb_exchange_token&client_id={}&client_secret={}&fb_exchange_token={}'
	url = base_url.format(app_id, app_secret, access_token)
	r = requests.get(url)
	return r

def validate_url(url):
    final_url = urlparse(urljoin(url, "/"))
    valid = (all([final_url.scheme, final_url.netloc, final_url.path]) 
              and len(final_url.netloc.split(".")) > 1)
    return valid


def write_location(lat, lon):
    path = os.path.abspath("location")
    location = {}
    location["latitude"] = lat
    location["longitude"] = lon

    with open(path, 'w') as store:
        json.dump(location, store, ensure_ascii = False, indent = 4)

def write_number(num):
    path = os.path.abspath("number")
    number = {}
    number["number"] = num

    with open(path, 'w') as store:
        json.dump(num, store, ensure_ascii = False, indent = 4)

def create_post():
    pass

headers = {
	'Content-Type' : 'application/json'
}


def post_photo(id, url, token):
    data = json.dumps({
        'url': url,
        'message': "Good afternoon! Here's what we have to offer at Aarifu today!\nPlease contact us at +254753232567 to find out more!"
    })
    fb = 'https://graph.facebook.com/{0}/photos?spublished=true&access_token={2}'.format(id, url, token)

    r = requests.post(fb, headers = headers, data= data)
    response = json.loads(r.content)
    return response
