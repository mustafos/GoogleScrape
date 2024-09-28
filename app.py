from flask import Flask, request, jsonify, render_template
import git
import logging
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

logging.basicConfig(filename='/home/mustafos/webhook.log', level=logging.INFO)

# Route to update the server via webhook
@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            logging.info('Received webhook request')
            repo = git.Repo('/home/mustafos/GoogleScrape')  # Use absolute path
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
    return render_template('index.html')  # Make sure 'index.html' is in the 'templates' folder

# Route to handle the search request
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    url = f'https://www.google.com/search?q={query}'

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

    # Parsing organic search results
    results = []
    for g in soup.find_all('div', class_='g'):
        title = g.find('h3')
        link = g.find('a')
        if title and link:
            results.append({
                'title': title.text,
                'link': link['href']
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
