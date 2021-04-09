#!/usr/bin/python3 

from pathlib import Path

import requests

MODEL_PATH = Path('model.pickle')
MODEL_ID = '1GLAmnK2DMRf9j1Fs2cnls-O9m3G-xj2Q'


# taken from this StackOverflow answer: https://stackoverflow.com/a/39225039
def download_file_from_google_drive(file_id=MODEL_ID, destination=MODEL_PATH):
    url = "https://docs.google.com/uc?export=download"

    session = requests.Session()
    params = {'id': file_id}

    response = session.get(url, params=params, stream=True)

    if token := get_confirm_token(response):
        params['confirm'] = token
        response = session.get(url, params=params, stream=True)

    save_response_content(response, destination)    

    
def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value
    return None


def save_response_content(response, destination, chunk_size=32768):
    # filter out keep-alive new chunks
    chunks = (chunk for chunk in response.iter_content(chunk_size) if chunk)

    with destination.open('wb') as file:
        for chunk in chunks:
            file.write(chunk)
            

def main():
    print('running download script')
    if not MODEL_PATH.exists():
        print('downloading data')
        download_file_from_google_drive()
    else:
        print('model exists')

        
if __name__ == '__main__':
    main()
