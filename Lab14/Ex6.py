# Retrieve the Hawaii mortgage-rates page using requests
import requests


url = "https://www.hicentral.com/hawaii-mortgage-rates.php"

try:
    response = requests.get(
        url,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    response.raise_for_status()
except requests.RequestException as error:
    print(f"Could not retrieve mortgage-rate information: {error}")
    raise SystemExit(1) from error

print(f"Retrieving {url}")
print(f"Status code: {response.status_code}")
print(f"Content type: {response.headers.get('Content-Type')}")
print(f"Response length: {len(response.text):,} characters")

print("\nPage title:")
print("Hawaii Mortgage Rates")

print("\nFirst 500 characters:")
print(response.text[:500])
