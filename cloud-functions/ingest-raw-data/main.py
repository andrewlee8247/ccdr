import os
import requests
from bs4 import BeautifulSoup
import xlrd
import csv
from io import BytesIO
from google.cloud import storage
from google.cloud.storage import Blob


def upload_raw_uci(event, context):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('ccdr-raw')
    url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/00350/'
    headers = {'User-Agent': "Chrome/54.0.2840.90"}
    response = requests.get(url, headers=headers)
    html = response.content
    soup = BeautifulSoup(html, 'html.parser')
    tmpRow = soup.findAll('a')
    for i in range(len(tmpRow)):
        if tmpRow[i]['href'][-4:] == '.xls':
            get_file = requests.get(url + tmpRow[i]['href'], headers=headers)
            file_name = tmpRow[i]['href'][:-4] + '.csv'
            convert = BytesIO(get_file.content)
            book = xlrd.open_workbook(file_contents = convert.getvalue())
            sh = book.sheet_by_name('Data')
            outfile = open('/tmp/' + file_name, 'w')
            wr = csv.writer(outfile)
            for rownum in range(sh.nrows):
                wr.writerow(sh.row_values(rownum))
            outfile.close()
            blob = Blob('uci/' + file_name, bucket)
            with open('/tmp/' + file_name, 'rb') as my_file:
                blob.upload_from_file(my_file)
            os.remove('/tmp/' + file_name)
        elif tmpRow[i]['href'][-4:] == '.csv':
            file_name = tmpRow[i]['href'] 
            open('tmp/' + file_name, 'wb').write(get_file.content)
            blob = Blob('uci/' + file_name, bucket)
            with open('/tmp/' + file_name, 'rb') as my_file:
                blob.upload_from_file(my_file)
            os.remove('/tmp/' + file_name)
    return
