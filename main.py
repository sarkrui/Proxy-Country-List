import requests
from geoip2.database import Reader
import os
import subprocess
from collections import OrderedDict


# Path to GeoLite2-Country.mmdb database file
path_to_db = './GeoLite2-Country.mmdb'

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
                # Prepend "socks5://" if it's not already there
                if not proxy.startswith('socks5://'):
                    proxy = 'socks5://' + proxy
                f.write(proxy + '\n')

def check_proxies(filtered_proxies, repo_name, source):
    valid_dir = f'{repo_name}/valid'
    os.makedirs(valid_dir, exist_ok=True)

    # Create a temporary file for the proxies and write them into the file
    with open('temp_proxies.txt', 'w') as f:
        f.writelines("\n".join(get_socks5_proxies(source['urls'])))

    for country_code in filtered_proxies.keys():
        filename = f'{repo_name}/socks5/socks5_{country_code.lower()}.txt'
        output_filename = f'{valid_dir}/valid_socks5_{country_code.lower()}.txt'
        
        subprocess.run(['./proxy-check', '-r', '-m', '30', '--socks5', '-o', output_filename, '-f', filename])

        # Open the file and remove the lines with errors
        with open(output_filename, 'r') as f:
            lines = f.readlines()

        # Replace 'error code: 1015' with 'error code: 1015\n' to add a return mark
        lines = [line.replace('error code: 1015', 'error code: 1015\n') for line in lines]

        # Filter out lines containing the error
        lines = [line for line in lines if 'socks5://error code: 1015' not in line]

        # Remove duplicate lines while preserving order
        lines = list(OrderedDict.fromkeys(lines))

        # Write the filtered lines back to the file
        with open(output_filename, 'w') as f:
            f.writelines(lines)

    # Remove the temporary file after finishing
    os.remove('temp_proxies.txt')


def main():

    for source in repo_sources:
        proxies = get_socks5_proxies(source['urls'])
        filtered_proxies = filter_by_country(proxies)
        save_proxies(filtered_proxies, source['name'])
        check_proxies(filtered_proxies, source['name'], source)

if __name__ == '__main__':
    main()