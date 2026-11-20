# Scrape data from the City of Chicago's data portal
# Print any line containing a <title> tag
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://data.cityofchicago.org/Historic-Preservation/Landmark-Districts/zidz-sdfj/about_data"

print(f"Retrieving {url}")
response = urllib.request.urlopen(url)

for line in response:
    decoded_line = line.decode("utf-8")
    if "<title" in decoded_line.lower():
        print(decoded_line.strip())

