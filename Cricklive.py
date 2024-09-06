from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_cricket_score():
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find relevant section using inspect tool, adjust according to website
    matches = soup.find_all('div', class_='html-refresh ng-isolate-scope')  # Example: Adjust according to the actual tags
    scores = []

    for match in matches:
        match_title = match.find('h3', class_='cb-nav-main cb-col-100 cb-col cb-bg-white').text.strip()
        match_score = match.find('div', class_='cb-col-100 cb-col cb-col-scores').text.strip()
        scores.append({'match': match_title, 'score': match_score})

    return scores

@app.route('/score', methods=['GET'])
def score():
    try:
        live_scores = get_cricket_score()
        return jsonify({'status': 'success', 'scores': live_scores})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
