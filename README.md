# GoogleScrape

[![Header](https://github.com/mustafos/GoogleScrape/blob/master/illustration/banner.gif)](https://mustafos.pythonanywhere.com)

GoogleScrape is a simple web application designed to fetch and parse organic search results from Google. The application provides a user-friendly interface with an input field where you can enter a search query, and it returns the results from the first page of Google's organic search in a structured format. This project demonstrates the ability to scrape web data without using the official Google API.

## Features
- **User Input**: Allows users to enter a search query through a web-based form.
- **Search Parsing**: Extracts and displays the organic search results (title and URL) from the first page of Google search.
- **JSON Output**: Returns the parsed results in a machine-readable JSON format for easy storage and processing.
- **Server-Side Processing**: Uses a Python-based backend (Flask) to handle web scraping and data parsing.
- **Data Privacy**: No Google API usage; data is extracted directly from the search results page.

## Tech Stack
- **Frontend**: HTML, JavaScript (Fetch API)
- **Backend**: Python (Flask, BeautifulSoup, Requests)
- **Output**: JSON data format

[![Body](https://github.com/mustafos/GoogleScrape/blob/master/illustration/summary.gif)](https://mustafos.pythonanywhere.com)

## Prerequisites
- Python 3.x
- Flask
- BeautifulSoup4
- Requests

## How to Use
1. **Clone the repository.**
2. **Install the required Python packages:**
```bash
pip install flask beautifulsoup4 requests
```
3. **Run the Flask server:**
```bash
python app.py
```
4. **Open a web browser and go to** [`https://mustafos.pythonanywhere.com`](https://mustafos.pythonanywhere.com)
5. **Enter a search query in the input field and click `Search`.**
6. **The results from the first page of Google’s organic search will be displayed in JSON format.**

## Disclaimer
This project is intended for educational and personal use only. Scraping Google’s search results directly may violate their terms of service, and heavy usage can result in IP blocking. Use this application responsibly and at your own risk.
