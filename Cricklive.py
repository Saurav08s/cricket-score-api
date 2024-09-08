import requests 
from bs4 import BeautifulSoup 
from flask import Flask, jsonify 

app = Flask(__name__) 


@app.route('/') 
def cricgfg(): 
    html_text = requests.get('https://www.cricbuzz.com/cricket-match/live-scores').text 
    soup = BeautifulSoup(html_text, "html.parser") 
    sect = soup.find_all('div', class_='cb-scr-wll-chvrn cb-lv-scrs-col ') 
    if len(sect) == 0:
        return jsonify({"error": "No live matches found."})
    
    # Use the first section found (if exists)
    section = sect[0]
    
    description = section.find('h2', class_='cb-lv-grn-strip text-bold cb-lv-scr-mtch-hdr').text 
    location = section.find('span', class_='text-gray').text 
    current = section.find('div', class_='scr_dt-red').text 
    try: 
        status = section.find_all('div', class_="cb-text-complete")[1].text 
        block = section.find_all('div', class_='cb-scr-wll-chvrn cb-lv-scrs-col ') 
        team1_block = block[0] 
        team1_name = team1_block.find('div', class_='cb-ovr-flo cb-hmscg-tm-nm').text 
        team1_score = team1_block.find('div', class_='cb-ovr-flo').text 
        team2_block = block[1] 
        team2_name = team2_block.find('div', class_='cb-ovr-flo cb-hmscg-tm-nm').text 
        team2_score = team2_block.find('div', class_='cb-ovr-flo').text 
        result = { 
            "Description": description, 
            "Location": location, 
            "Current": current, 
            "Status": status, 
            "Team A": team1_name, 
            "Team A Score": team1_score, 
            "Team B": team2_name, 
            "Team B Score": team2_score, 
            "Credits": "Cricbuzz"
        } 
    except: 
        pass
    return jsonify(result) 

if __name__ == "__main__": 
    app.run(debug=True)
