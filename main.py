import requests
from geoip2.database import Reader
import os
import subprocess


# Path to GeoLite2-Country.mmdb database file
path_to_db = './GeoLite2-Country.mmdb'

def get_country(ip_address, reader):
    try:
        response = reader.country(ip_address)
        return response.country.iso_code
    except:
        return None

def get_socks5_proxies():
    url = "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt"
    response = requests.get(url)
    data = response.text
    return data.splitlines()

def filter_by_country(proxies):
    reader = Reader(path_to_db)
    filtered_proxies = {}

    for proxy in proxies:
        ip_address = proxy.split(':')[0]
        country = get_country(ip_address, reader)

        if country:
            if country not in filtered_proxies:
                filtered_proxies[country] = []
            filtered_proxies[country].append(proxy)

    return filtered_proxies

def save_proxies(filtered_proxies):
    socks5_dir = 'socks5'
    os.makedirs(socks5_dir, exist_ok=True)

    for country_code, proxies in filtered_proxies.items():
        with open(f'{socks5_dir}/socks5_{country_code.lower()}.txt', 'w') as f:
            for proxy in proxies:
                f.write(proxy + '\n')

def check_proxies(filtered_proxies):
    valid_dir = 'valid'
    os.makedirs(valid_dir, exist_ok=True)

    for country_code in filtered_proxies.keys():
        filename = f'socks5/socks5_{country_code.lower()}.txt'
        output_filename = f'{valid_dir}/valid_socks5_{country_code.lower()}.txt'
        
        subprocess.run(['./proxy-check', '-r', '-m', '30', '--socks5', '-o', output_filename, '-g', filename])


def main():
    proxies = get_socks5_proxies()
    filtered_proxies = filter_by_country(proxies)
    save_proxies(filtered_proxies)
    check_proxies(filtered_proxies)
    
if __name__ == '__main__':
    main()