from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

def get_cricket_score():
    url = "https://www.cricbuzz.com/cricket-match/live-scores"
    html_text = requests.get(url)
    soup = BeautifulSoup(html_text.text, 'html.parser')

    matches = soup.find_all('div', class_='cb-mtch-lst cb-col cb-col-100 cb-tms-itm')
    scores = []

    for match in matches:
        match_title = match.find('h3', class_='cb-lv-grn-strip text-bold cb-lv-scr-mtch-hdr').text.strip()
        match_score = match.find('div', class_='cb-col-100 cb-col cb-schdl').text.strip()
        scores.append({'match': match_title, 'score': match_score})

    return scores

@app.route('/score', methods=['GET'])
def score():
    try:
        live_scores = get_cricket_score()
        return render_template('index.html', scores=live_scores)
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
