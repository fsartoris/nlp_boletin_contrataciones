import os
import json
import pathlib
import logging

from urllib.parse import urlparse
#from google.cloud import storage

def get_bucket():
    return os.environ.get('BUCKET', None)

def running_on_cloud():
    if os.environ.get('CLOUD', None) == None:
        return False
    else: 
        return True

def persist_json(url, body, date):
    data = json.dumps({"url" : url, "body" : body}, ensure_ascii=False)
    o = urlparse(url)
    filename = date + "/" + "boletin" + o.path.replace("/", "_") + ".json"

    if not running_on_cloud():
        save_local(filename, data, date)
    else: 
        save_cloud(get_bucket(), data, filename)


def save_local(filename, data, date):
    try:
        if not os.path.exists(pathlib.Path.cwd() / 'data' / date):
            os.makedirs(pathlib.Path.cwd() / 'data' / date)

        path = pathlib.Path.cwd() / 'data' / filename
        with open(path, 'w+', encoding='latin-1') as outfile:
            json.dump(data, outfile)

    except Exception as e:
        logging.error('Error at %s', exc_info=e)
    

def save_cloud(bucket_name, source_file_name, destination_blob_name):
    if not running_on_cloud():
        storage_client = storage.Client()
    else:
        storage_client = storage.Client.from_service_account_json('credentials/storage.json')
    
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(source_file_name)


def get_files(fecha):
    if not running_on_cloud():
        return get_files_local(fecha)
    else:
        return get_files_cloud(fecha)

def get_files_local(fecha):
    path = pathlib.Path.cwd() / 'data' / fecha
    entries = os.listdir(path)
    return entries

def get_files_cloud(fecha):
    
    if not running_on_cloud():
        storage_client = storage.Client.from_service_account_json('credentials/storage.json')
    else:
        storage_client = storage.Client.from_service_account_json('credentials/storage.json')
        #storage_client = storage.Client()
    
    folder = fecha + '/'
    blobs = storage_client.list_blobs(get_bucket(), prefix=folder, delimiter='/')
    entries = []
    for blob in blobs:
        entries.append(blob.name)

    return entries


def get_file_content(fecha, filename):

    if running_on_cloud():   
        return get_file_content_cloud(filename)        
    else:
        return get_file_content_local(filename, fecha)
        

def get_file_content_cloud(filename):
    storage_client = storage.Client.from_service_account_json('credentials/storage.json')
    filepath = pathlib.Path.cwd() / 'tmp' / 'object.json'

    bucket = storage_client.bucket(get_bucket())
    blob = bucket.get_blob(filename)    
    blob.download_to_filename(filepath)

    with open(filepath, encoding='utf-8') as json_file:
        json_object = json.load(json_file)
        return json_object


def get_file_content_local(filename, fecha):
    filepath = pathlib.Path.cwd() / 'data' / fecha / filename
    
    with open(filepath, encoding='latin-1') as json_file:
        json_object = json.load(json_file)
        json_parsed = json.loads(json_object)
        return json_parsed