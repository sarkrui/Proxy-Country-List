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

def get_socks5_proxies(repo_urls):
    proxies = []
    for url in repo_urls:
        response = requests.get(url)
        data = response.text
        proxies.extend(data.splitlines())
    return proxies

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

def save_proxies(filtered_proxies, repo_name):
    socks5_dir = f'{repo_name}/socks5'
    os.makedirs(socks5_dir, exist_ok=True)

    for country_code, proxies in filtered_proxies.items():
        with open(f'{socks5_dir}/socks5_{country_code.lower()}.txt', 'w') as f:
            for proxy in proxies:
                f.write(proxy + '\n')

def check_proxies(filtered_proxies, repo_name):
    valid_dir = f'{repo_name}/valid'
    os.makedirs(valid_dir, exist_ok=True)

    for country_code in filtered_proxies.keys():
        filename = f'{repo_name}/socks5/socks5_{country_code.lower()}.txt'
        output_filename = f'{valid_dir}/valid_socks5_{country_code.lower()}.txt'
        
        subprocess.run(['./proxy-check', '-r', '-m', '50', '--socks5', '-o', output_filename, '-g', filename])

def main():
    repo_sources = [
        {
            'name': 'hookzof',
            'urls': ['https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt']
        },
        {
            'name': 'TheSpeedX',
            'urls': ['https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/socks5.txt']
        },
        # Add more sources as needed
    ]

    for source in repo_sources:
        proxies = get_socks5_proxies(source['urls'])
        filtered_proxies = filter_by_country(proxies)
        save_proxies(filtered_proxies, source['name'])
        check_proxies(filtered_proxies, source['name'])

if __name__ == '__main__':
    main()