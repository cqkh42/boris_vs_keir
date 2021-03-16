#!/usr/bin/python3 

from pathlib import Path

import requests

DEFAULT_MODEL_LOCATION = Path('model.pickle')
DEFAULT_MODEL_ID = '1GLAmnK2DMRf9j1Fs2cnls-O9m3G-xj2Q'

#taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
def download_file_from_google_drive(id=DEFAULT_MODEL_ID, destination=DEFAULT_MODEL_LOCATION):
    destination.unlink(missing_ok=True)
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    params = {'id': id}

    response = session.get(URL, params=params, stream=True)
    token = get_confirm_token(response)

    if token:
        params['confirm'] = token
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination, chunk_size=32768):
    # filter out keep-alive new chunks
    chunks = (chunk for chunk in response.iter_content(chunk_size) if chunk)

    with destination.open('wb') as f:
        for chunk in chunks:
            f.write(chunk)
            

def main():
    print('running download script')
    if not DEFAULT_MODEL_LOCATION.exists():
        print('downloading data')
        download_file_from_google_drive()
    else:
        print('model exists')

        
if __name__ == '__main__':
    main()