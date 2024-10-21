from flask import Flask, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import pytz
from datetime import datetime

app = Flask(__name__)
CORS(app)
timezone = pytz.timezone('Europe/Rome')

@app.route('/updates', methods=['GET'])
def check_updates():
    response = requests.get('https://conts.it/it/')
    soup = BeautifulSoup(response.text, 'html.parser')

    updates = []
    news_cards = soup.find_all('div', class='news-card')
    for card in news_cards:
        link = card.find('a')['href']
        full_url = f"https://conts.it{link}"
        date = card.find('p', class'news-date').get_text(strip=True)
        body = card.find('p', class'news-body').get_text(strip=True)
        updates.append({'date': date, 'body': body, 'url': full_url})

    current_time = datetime.now(timezone).strftime('%H:%M:%S %d-%m-%Y')
    return jsonify({'last_scan': current_time, 'updates': updates})

if __name__ == "__main__":
    app.run(debug=True)
