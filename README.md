# Socks5 Proxy Checker

This script fetches SOCKS5 proxy lists from different repositories, filters them by country using a GeoIP database, and checks the validity of the proxies. Valid proxies are saved for each country in separate files.

## Requirements

To run this script, you need the following:

- Python 3
- `requests` library (`pip3 install requests`)
- `geoip2` library (`pip3 install geoip2`)
- GeoLite2 Country database file (`GeoLite2-Country.mmdb`)
- `proxy-check` executable

The `proxy-check` executable is used for checking the validity of the SOCKS5 proxies. Make sure you have it installed and available in your PATH.

## Setup

1. Clone or download this repository to your local machine.

2. Install the required Python libraries by running the following command:

   ```bash
   pip3 install -r requirements.txt
	```

3.  Ensure that the `proxy-check` executable is installed and available in your PATH. You can download it from the appropriate source and make it executable if necessary.

Usage
-----

1.  Open a terminal or command prompt and navigate to the repository directory.
    
2.  Run the script by executing the following command:
    
    bash
    
    ```bash
    python3 main.py
	```

    The script will fetch SOCKS5 proxy lists from different repositories, filter them by country, and check their validity. Valid proxies will be saved in separate files based on the country code.

3.  After the script finishes, you can find the results in the following directories:
    
    *   `hookzof/socks5`: Contains the SOCKS5 proxy files for each country (e.g., `socks5_us.txt`).
    *   `hookzof/valid`: Contains the validated SOCKS5 proxy files for each country (e.g., `valid_socks5_us.txt`).
    
    Note: The directory names are based on the repository names defined in the script.
    

Customization
-------------

*   Adding or modifying repository sources: You can add or modify repository sources by extending or modifying the `repo_sources` list in the script. Each source should have a unique name and a list of URLs pointing to SOCKS5 proxy lists.
    
*   Changing the output directory: You can change the output directory names by modifying the `socks5_dir` and `valid_dir` variables in the script.
    
*   Adjusting proxy checking options: The script uses the `proxy-check` executable for proxy checking. You can modify the options passed to `proxy-check` by modifying the subprocess command in the `check_proxies` function.