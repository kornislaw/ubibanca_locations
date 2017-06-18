"""
The current UBI Banca's website does not work properly in many web browsers.
Browser-based scrapers cannot handle collecting locations.

This short script collects locations both in JSON and CSV formats.
"""

from json_to_csv import json_to_csv
import json
import requests
import time
from bs4 import BeautifulSoup


def prepare_input_query(province):
    return [
        ('banksString', '4|1|3|9|8|10'),
        ('province', province),
        ('address', ''),
        ('city', ''),
        ('cap', ''),
        ('abi', ''),
        ('cab', ''),
        ('start', '0'),
        ('end', '1000'),
        ('serviceClassName',
         'it.reply.open.ubi.backend.filiale.service.UBIFilialeServiceUtil'),
        ('serviceMethodName', 'findByFilialiConLista'),
        ('serviceParameters',
         'banksString,province,address,city,cap,abi,cab,start,end'),
    ]


def post_query(data):
    r = requests.post('https://www.ubibanca.com/page/c/portal/json_service', data=data)
    return json.loads(r.text)


def get_provinces():
    """ Getting a list of all provinces. It is reuse as input in further locations search. """
    loc_form_url = "https://www.ubibanca.com/page/web/community-mail/fissaappuntamento"
    r = requests.get(loc_form_url)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    result = soup.select('#provincia > option')
    return [r.text for r in result[1:]]


def main():
    locs = []
    for province in get_provinces():
        data = prepare_input_query(province)
        res = post_query(data)
        print(f'{province}: {len(res)}')
        if len(res) > 0:
            locs += res
        time.sleep(2)  # break between requests to not overload the site
    with open('res.json', 'w') as f:  # store output in json
        f.write(json.dumps(locs))
    json_to_csv('res.json', 'res.csv')  # store output in csv


if __name__ == '__main__':
    main()
