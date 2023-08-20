from flask import Flask, render_template, jsonify, request
from googleapiclient.discovery import build

app = Flask(__name__)

API_KEY = 'AIzaSyCgwhPlyWmVoJJIrZHWwUqi0SkiHjTNHEk'
SEARCH_ENGINE_ID = '62f1d66bfbaa74fe4'

def search_custom(query):
    service = build('customsearch', 'v1', developerKey=API_KEY)
    result = service.cse().list(q=query, cx=SEARCH_ENGINE_ID).execute()
    return result.get('items', [])

@app.route('/get_search_results', methods=['GET', 'POST'])
def get_search_results():
    if request.method == 'POST':
        query = request.form['search_query']
        results = search_custom(query)

        articles_with_data = []
        for result in results:
            articles_with_data.append({
                'title': result['title'],
                'link': result['link'],
                'snippet': result['snippet']
            })

        return jsonify(articles_with_data)

    return jsonify([])

@app.route('/')
def index():
    query = "hacking issues today"
    results = search_custom(query)

    articles_with_data = []
    for result in results:
        articles_with_data.append({
            'title': result['title'],
            'link': result['link'],
            'snippet': result['snippet']
        })

    return render_template('index.html', articles=articles_with_data)

if __name__ == "__main__":
    app.run(debug=True)
