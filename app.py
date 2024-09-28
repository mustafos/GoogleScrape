from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

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
