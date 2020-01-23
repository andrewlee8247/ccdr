from flask import Flask
from flask import jsonify
from google.cloud import storage
import pandas as pd
from io import BytesIO


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


@app.route('/')
def home():
    """Returns home page HTML"""
    return """
    <!DOCTYPE html>
    <head>
    <title>Credit Card Default Risk App</title>
    <style>
    .content{
        max-width: 500px;
        margin: auto;
    }
    .button {
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 25px;
        text-align: center;
        font-size: 16px;
        cursor: pointer;
    }
    .button:hover {
        background-color: green;
    }
    </style>
    </head>
    <body>
    <div class="content">
    <h2>This app will predict if a cardholder will default
    on their next payment.</h2>
    <a href="https://ccdr-265306.appspot.com/cardholder/data">
    <button class="button">Click to View JSON Data</button></a>
    </div>
    </body>
    </html>
    """


@app.route('/cardholder/data')
def raw_data():
    """Returns raw cardholder data as JSON response"""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("ccdr-raw")
    blobs = bucket.list_blobs()
    data = pd.DataFrame()
    for blob in blobs:
        file = blob.download_as_string()
        data = data.append(pd.read_csv(BytesIO(file)))
    data.reset_index(drop=True, inplace=True)
    return jsonify(data.to_dict())


if __name__ == '__main__':
    app.run()
