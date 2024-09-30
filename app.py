from flask import Flask, request, jsonify, render_template
import git
import logging
import requests
import urllib.parse
from bs4 import BeautifulSoup

app = Flask(__name__)

logging.basicConfig(filename='/home/mustafos/webhook.log', level=logging.INFO)

# Route to update the server via webhook
@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            logging.info('Received webhook request')
            repo = git.Repo('/home/mustafos/GoogleScrape')
            origin = repo.remotes.origin
            origin.pull()
            logging.info('Repository updated successfully')
            return 'Updated PythonAnywhere successfully', 200
        except Exception as e:
            logging.error(f'Error during Git pull: {str(e)}')
            return f'An error occurred: {str(e)}', 400
    else:
        return 'Wrong event type', 400

# Route to serve the HTML file
@app.route('/')
def home():
    return render_template('index.html')

# Method to find organic search results with multiple class checks
def find_results(soup):
    # Expanded list of potential classes for organic results
    potential_classes = [
        'tF2Cxc',  # Main class for organic results
        'g',       # A common class used in organic results
        'rc',      # Another commonly seen class in older Google pages
        'ZINbbc',  # Used for certain types of result blocks
        'v7W49e',  # Used for some featured snippets
        'xpd',     # Expanded information panels
        'MjjYud',  # Organic results container in some versions
        'yuRUbf',  # Link container for some organic results
        'BVG0Nb'   # Title container in some search blocks
    ]

    results = []
    for class_name in potential_classes:
        # Attempt to find elements with the current class name
        for result_block in soup.find_all('div', class_=class_name):
            title_element = result_block.find('h3')
            link_element = result_block.find('a')
            
            if title_element and link_element:
                title = title_element.get_text()
                link = link_element['href']
                
                # Clean up the Google redirect URL
                if '/url?' in link:
                    link = urllib.parse.parse_qs(urllib.parse.urlparse(link).query).get('url', [None])[0]
                
                if link:
                    results.append({'title': title, 'link': link})
        
        # If results are found, return them
        if results:
            logging.info(f"Found results using class: {class_name}")
            return results

    # If no results are found with any of the classes, return an empty list
    logging.warning('No results found with any of the known classes.')
    return []

# Route to handle the search request
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    url = f'https://www.google.com/search?q={query}&hl=en'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if the request was successful
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching Google results: {str(e)}')
        return jsonify({'error': 'Failed to fetch search results'}), 500
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Save the HTML to a file for debugging
    with open('/home/mustafos/google_search_debug.html', 'w', encoding='utf-8') as file:
        file.write(response.text)
    
    # Use the find_results method to get search results
    results = find_results(soup)
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
