from google.cloud import storage
from google.cloud import bigquery


def upload_to_bq(event, context):
    # Upload data files into BigQuery
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("ccdr-cleaned")
    blobs = bucket.list_blobs()

    file_names = []
    for blob in blobs:
        file_names.append(blob.name)
    for i in range(len(file_names)):
        database = 'ccdr-265306'
        bigquery_client = bigquery.Client(database)
        dataset = bigquery_client.dataset('ccdr_database')
        table = dataset.table('cardholder_data')
        job_config = bigquery.LoadJobConfig(write_disposition = "WRITE_TRUNCATE")
        job_config.source_format = bigquery.SourceFormat.PARQUET
        job = bigquery_client.load_table_from_uri('gs://ccdr-cleaned/' + file_names[i], 
                                                  table, job_config = job_config)
        job.job_id
        job.result()
        if job.state == 'DONE':
            print("state of job is: " + job.state)
        else: 
            print(job.errors)
    return
