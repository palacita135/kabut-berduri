import requests
from bs4 import BeautifulSoup
import re
import shodan
import pandas as pd

# Set your Shodan API key
SHODAN_API_KEY = 'YOUR_SHODAN_API_KEY'

# Regex patterns for email, phone number, and address
EMAIL_REGEX = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}'
PHONE_REGEX = r'(\+?\d{1,2}\s?)?(\(?\d{1,4}\)?[\s\-]?)?(\d{1,4}[\s\-]?\d{1,4}[\s\-]?\d{1,4})'
ADDRESS_REGEX = r'\d+\s[A-z]+\s[A-z]+(?:\s[A-z]+)*'  # Basic address pattern

# Function to scrape emails from a website
def scrape_emails(url):
    emails = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all email-like strings
        for string in soup.stripped_strings:
            found_emails = re.findall(EMAIL_REGEX, string)
            if found_emails:
                emails.extend(found_emails)
        
        return list(set(emails))  # Remove duplicates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Function to scrape phone numbers from a website
def scrape_phone_numbers(url):
    phone_numbers = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all phone number-like strings
        for string in soup.stripped_strings:
            found_numbers = re.findall(PHONE_REGEX, string)
            if found_numbers:
                phone_numbers.extend(found_numbers)
        
        return list(set(phone_numbers))  # Remove duplicates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Function to scrape addresses from a website
def scrape_addresses(url):
    addresses = []
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all address-like strings
        for string in soup.stripped_strings:
            found_addresses = re.findall(ADDRESS_REGEX, string)
            if found_addresses:
                addresses.extend(found_addresses)
        
        return list(set(addresses))  # Remove duplicates
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Function to search for devices globally using Shodan
def search_shodan(query):
    devices = []
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        results = api.search(query)
        
        for result in results['matches']:
            devices.append({
                'IP': result['ip_str'],
                'Location': result.get('location', {}).get('country_name', 'N/A'),
                'Data': result['data']
            })
        
        return devices
    except shodan.ShodanAPIError as e:
        print(f"Shodan API Error: {e}")
        return []

# Function to save results to CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function to run the OSINT tool
def main():
    # Example website URLs to scrape for emails, phone numbers, and addresses
    websites = ['https://example.com', 'https://anotherexample.com']
    
    all_results = []
    
    # Scrape emails, phone numbers, and addresses from websites
    for website in websites:
        print(f"Scraping {website} for emails...")
        emails = scrape_emails(website)
        for email in emails:
            all_results.append({'Source': website, 'Type': 'Email', 'Data': email})
        
        print(f"Scraping {website} for phone numbers...")
        phone_numbers = scrape_phone_numbers(website)
        for phone in phone_numbers:
            all_results.append({'Source': website, 'Type': 'Phone Number', 'Data': phone})
        
        print(f"Scraping {website} for addresses...")
        addresses = scrape_addresses(website)
        for address in addresses:
            all_results.append({'Source': website, 'Type': 'Address', 'Data': address})
    
    # Search for devices globally using Shodan
    print("Searching for devices worldwide using Shodan...")
    shodan_results = search_shodan('port:80')  # You can modify this search query as needed
    for device in shodan_results:
        all_results.append({'Source': 'Shodan', 'Type': 'IP', 'Data': device['IP']})
    
    # Save results to a CSV file
    save_to_csv(all_results, 'osint_results.csv')

# Run the OSINT tool
if __name__ == '__main__':
    main()
