import requests
from geoip2.database import Reader

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
    for country_code, proxies in filtered_proxies.items():
        with open(f'socks5_{country_code.lower()}.txt', 'w') as f:
            for proxy in proxies:
                f.write(proxy + '\n')

def main():
    proxies = get_socks5_proxies()
    filtered_proxies = filter_by_country(proxies)
    save_proxies(filtered_proxies)

if __name__ == '__main__':
    main()