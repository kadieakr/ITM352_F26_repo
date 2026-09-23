url = input("Enter a URL: ")

# Remove http:// or https:// from the beginning of the URL
url = url.replace("http://", "").replace("https://", "")

domain = url.split("/")[0]  # Get the domain part of the URL
tld = domain.split(".")[-1]  # Get the top-level domain (TLD)   

print("Domain name:", domain)
print("Top-level domain:", tld)     
