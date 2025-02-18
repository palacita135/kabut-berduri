# kabut-berduri
# script Python untuk OSINT yang fokus pada pencarian data di Indonesia

       1.Web Scraping untuk mencari data dari sumber terbuka, seperti website Indonesia (misalnya, data alamat atau kontak).
       2.Shodan untuk mencari perangkat yang terhubung ke internet di Indonesia.
       3.Pandas untuk menganalisis data yang ditemukan, seperti daftar domain atau alamat IP.


# Penjelasan:
# Scraping Website: Mengambil data link dari halaman web Indonesia menggunakan requests dan BeautifulSoup. Semua link yang mengandung id di dalam URL akan dipilih, yang umumnya mencirikan situs Indonesia.
# Shodan: Menggunakan API Shodan untuk mencari perangkat yang terhubung ke internet di Indonesia berdasarkan negara (country:ID). Kamu perlu mengganti YOUR_SHODAN_API_KEY dengan API key milikmu.
# Pandas: Hasil dari web scraping dan pencarian perangkat Shodan digabungkan menjadi satu set data dan disimpan dalam file CSV menggunakan pandas.

# Langkah-langkah:
# Instalasi Dependencies: Pastikan pustaka yang diperlukan sudah terinstal:

    pip install requests beautifulsoup4 shodan pandas

# Shodan API Key: Kamu perlu mendaftar di Shodan untuk mendapatkan API key yang dapat digunakan untuk melakukan pencarian perangkat di internet.

# Catatan:
# Penggunaan API Shodan: Ada batasan pada jumlah pencarian gratis, jadi pastikan kamu menggunakan API dengan bijak.
# Perlu disesuaikan: Kamu dapat menambahkan fitur lain, seperti analisis lebih lanjut pada data yang ditemukan, menggabungkan teknik lain untuk memperoleh informasi lebih mendalam, dan menambahkan sumber lain untuk web scraping.
