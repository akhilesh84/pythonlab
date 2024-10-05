from flask import Flask, jsonify, render_template
import json, random, requests

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def api_endpoint():
    quotes = json.load(open('quotes.json'))
    random_quote = random.choice(quotes)
    return jsonify(random_quote)

@app.route('/api/quote', methods=['GET'])
def get_random_quote():
    quote = requests.get('https://api.quotable.io/random').json()
    return jsonify(quote)

if __name__ == '__main__':
    app.run(debug=True)
