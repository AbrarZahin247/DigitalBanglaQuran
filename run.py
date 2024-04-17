from flask import Flask, jsonify, request
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Function to execute SQL query and fetch data
def fetch_data_from_db(sura_name):
    conn = sqlite3.connect('alquran.db')
    c = conn.cursor()
    c.execute("SELECT ayat_no,bangla_ayat,arabic FROM Ayats WHERE sura_name=?", (sura_name,))
    data = c.fetchall()
    conn.close()
    return data

    
def search_keyword(keyword):
    conn = sqlite3.connect('alquran.db')
    c = conn.cursor()
    c.execute("SELECT ayat_no,sura_name,bangla_ayat FROM Ayats WHERE bangla_ayat LIKE ?", ('%' + keyword + '%',))
    data = c.fetchall()
    conn.close()
    return data

def fetch_all_sura_names():
    conn = sqlite3.connect('alquran.db')
    c = conn.cursor()
    c.execute("SELECT DISTINCT sura_name FROM Ayats")
    data = c.fetchall()
    conn.close()
    return [row[0] for row in data]

@app.route('/')
def hello():
    return 'Hello'

@app.route('/sura/<name>', methods=['GET'])
def get_sura_data(name):
    # Fetch data from the database based on the provided sura name
    data = fetch_data_from_db(name)

    # Check if data is found
    if data:
        # Prepare the response
        response = {
            'status': 'success',
            'data': data
        }
        return jsonify(response), 200
    else:
        # Sura not found
        response = {
            'status': 'error',
            'message': 'Sura not found'
        }
        return jsonify(response), 404

@app.route('/search/<keyword>', methods=['GET'])
def search(keyword):
    # Get the keyword from the request query parameters
    # keyword = request.args.get('keyword', '')

    # Search for the keyword in the "bangla_ayat" column
    data = search_keyword(keyword)

    # Prepare the response
    response = {
        'status': 'success',
        'data': data
    }
    return jsonify(response), 200

@app.route('/suranames', methods=['GET'])
def get_all_sura_names():
    # Fetch all unique sura names
    sura_names = fetch_all_sura_names()

    # Prepare the response
    response = {
        'status': 'success',
        'data': sura_names
    }
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True,port=7654)