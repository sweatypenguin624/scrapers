
# 🕷️ Web Scrapers Collection

Welcome to the **Web Scrapers Collection**! This repository houses a set of Python-based web scrapers designed to extract product data from various e-commerce platforms like **Flipkart** and **IndiaMART**. Whether you're conducting market research, price comparison, or data analysis, these tools can help you gather the necessary information efficiently.

---

## 📦 Repository Contents

```
scrapers/
├── flip.py                             # Flipkart scraper script
├── flipkart_scraper.log                # Log file for Flipkart scraper
├── indiamart_<query>_<timestamp>.csv   # CSV files with scraped IndiaMART data
├── indiamart_<query>_<timestamp>.txt   # Raw text files of IndiaMART data
├── debug_page_1.png                    # Screenshot for debugging
├── .gitignore                          # Git ignore file
└── .DS_Store                           # macOS directory metadata
```

---

## 🚀 Features

- 🛒 **Flipkart Scraper**: Extract product details such as name, price, and ratings from Flipkart listings.
- 🏭 **IndiaMART Scraper**: Gather supplier information, product specifications, and pricing from IndiaMART search results.
- 📄 **Data Storage**: Save extracted data in both `.csv` and `.txt` formats for easy analysis and record-keeping.
- 🐞 **Debugging Tools**: Utilize screenshots and log files to troubleshoot and ensure accurate data extraction.

---

## 🛠️ Getting Started

### Prerequisites

- [Python 3.7+](https://www.python.org/downloads/)
- Required Python libraries:
  - `requests`
  - `BeautifulSoup4`
  - `pandas`
  - `lxml` (optional, for faster HTML parsing)

Install the required libraries using pip:

```bash
pip install requests beautifulsoup4 pandas lxml
```

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/sweatypenguin624/scrapers.git
   cd scrapers
   ```

2. **Run the desired scraper:**

   - **Flipkart Scraper:**

     ```bash
     python flip.py
     ```

   - **IndiaMART Scraper:**

     *(Assuming there's a script named `indiamart.py`)*

     ```bash
     python indiamart.py
     ```

   *Note: Replace the script names with the actual filenames if they differ.*

---

## 🧠 How It Works

### Flipkart Scraper (`flip.py`)

1. Sends HTTP requests to Flipkart search result pages.
2. Parses the HTML content using BeautifulSoup.
3. Extracts product details such as:
   - Product Name
   - Price
   - Ratings
4. Stores the extracted data in a structured format (e.g., CSV).

### IndiaMART Scraper

1. Sends HTTP requests to IndiaMART search result pages based on user-defined queries.
2. Parses the HTML content to extract:
   - Supplier Name
   - Product Details
   - Contact Information
3. Saves the data in both `.csv` and `.txt` formats for versatility.

---

## 📁 Data Output

- **CSV Files**: Structured data suitable for analysis in tools like Excel or pandas.
- **Text Files**: Raw data for quick viewing or further processing.

Each output file is named using the format:

```
indiamart_<search_query>_<YYYYMMDD_HHMMSS>.csv
```

Example:

```
indiamart_cotton_shirts_20250414_224934.csv
```

---

## 🖼️ Debugging Aids

- **`debug_page_1.png`**: Screenshot of a sample page to assist in verifying the scraper's accuracy.
- **`flipkart_scraper.log`**: Log file capturing the scraper's runtime information and any errors encountered.

---

## ⚠️ Disclaimer

- Ensure compliance with the terms of service of Flipkart and IndiaMART when using these scrapers.
- Use responsibly and ethically. The author is not responsible for any misuse of the scripts.

---

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or additional features, feel free to fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Sweaty Penguin**  
GitHub: [@sweatypenguin624](https://github.com/sweatypenguin624)
