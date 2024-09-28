from flask import Flask, request, jsonify, render_template
import git
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route to update the server via webhook
@app.route('/update_server', methods=['POST'])
def webhook():
    if request.method == 'POST':
        try:
            repo = git.Repo('GoogleScrape')
            origin = repo.remotes.origin
            origin.pull()
            return 'Updated PythonAnywhere successfully', 200
        except Exception as e:
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

    response = requests.get(url, headers=headers)
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
