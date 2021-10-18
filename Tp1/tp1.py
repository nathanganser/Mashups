import json
import requests
import json
import country_converter
import xml.etree.ElementTree as ET


def get_country_ip(ip):
    endpoint = f'https://ipinfo.io/{ip}/json'
    response = requests.get(endpoint, verify = True)
    if response.status_code != 200:
        return 'Status:', response.status_code, 'Problem with the request. Exiting.'

    data = response.json()
    #print(data)

    return data.get('country')

def convert_country(country_code):
    return country_converter.convert(names=[country_code], to='ISO2')


def find_addresses_with_country(country_code):
    list = []
    with open('btc_address.json') as btc:
        data = json.load(btc)
        for p in data:
            #print(f"comparing: {convert_country(p.get('country'))} and {country_code}")
            if convert_country(p.get('country')) == country_code:
                list.append(p.get('btc_address'))
    return list

def get_fav_stock():
    tree = ET.parse('fav_stock.xml')
    root = tree.getroot()
    data = {}
    for el in range(0, 1000, +1):
        data[root[el][0].text] = root[el][1].text
    #print(data)
    return data


def people_to_btc():
    with open('people.json') as people:
        data = json.load(people)
        stock_info = get_fav_stock()
        for p in data:
            ip = p.get('ip_address')
            country_code = get_country_ip(ip)
            addresses = find_addresses_with_country(country_code)
            print(f"The possible btc addresses for {p.get('first_name')} {p.get('last_name')} are {addresses}")
            print(f"and the favorite stock for this person is {stock_info.get(p.get('first_name'))} (None means 'unkown', aka we don't have that first name in the database")



people_to_btc()


