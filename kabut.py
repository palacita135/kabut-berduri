import requests
from bs4 import BeautifulSoup
import shodan
import pandas as pd

# Set your Shodan API key
SHODAN_API_KEY = 'YOUR_SHODAN_API_KEY'

# Fungsi untuk scraping data dari website Indonesia
def scrape_indonesia_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, 'html.parser')

        # Mencari semua link (anchor tags) di halaman tersebut
        links = [a.get('href') for a in soup.find_all('a', href=True)]

        # Filter untuk link yang mungkin relevan
        indonesia_links = [link for link in links if 'id' in link]
        return indonesia_links
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

# Fungsi untuk mencari IP atau perangkat di Indonesia menggunakan Shodan
def search_shodan_in_indonesia(query):
    try:
        api = shodan.Shodan(SHODAN_API_KEY)
        results = api.search(query)
        indonesia_devices = []

        for result in results['matches']:
            # Menambahkan data perangkat yang ditemukan
            ip = result['ip_str']
            location = result.get('location', {}).get('country_name', '')
            if location == 'Indonesia':
                indonesia_devices.append({'IP': ip, 'Data': result['data']})
        
        return indonesia_devices
    except shodan.ShodanAPIError as e:
        print(f"Error with Shodan API: {e}")
        return []

# Fungsi untuk menyimpan hasil ke file CSV
def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main function untuk menjalankan OSINT di Indonesia
def main():
    # 1. Web scraping untuk mencari data dari situs Indonesia
    indonesia_website = 'https://www.example.co.id'  # Ganti dengan situs yang relevan
    print(f"Scraping website: {indonesia_website}")
    links = scrape_indonesia_website(indonesia_website)
    print(f"Found {len(links)} links on {indonesia_website}")

    # 2. Mencari perangkat atau data dengan Shodan di Indonesia
    print("Searching for devices in Indonesia using Shodan...")
    shodan_results = search_shodan_in_indonesia('country:ID')  # 'country:ID' untuk Indonesia
    print(f"Found {len(shodan_results)} devices in Indonesia.")

    # 3. Menggabungkan hasil dan menyimpan ke CSV
    combined_data = []
    for link in links:
        combined_data.append({'Source': 'Website', 'Data': link})
    for device in shodan_results:
        combined_data.append({'Source': 'Shodan', 'Data': device['IP']})

    # Simpan hasil ke file CSV
    save_to_csv(combined_data, 'indonesia_osint_data.csv')

# Menjalankan script
if __name__ == '__main__':
    main()
