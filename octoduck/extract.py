import os
from datetime import datetime

import requests


def get_url_file_path(active_datetime):
    url_datetime = datetime.strftime(active_datetime, "%Y-%m-%d-%-H")
    url = f"https://data.gharchive.org/{url_datetime}.json.gz"
    file_path = f"./data/{url_datetime}.json.gz"
    return url, file_path


def download_data(active_datetime):
    # Github Archive URL requires a non-zero-padded hour format
    # ChatGPT tells me '%-H' doesn't work on Windows,
    # but I don't have a Windows machine to test it on so lmk
    url, file_path = get_url_file_path(active_datetime)
    if not os.path.exists(file_path):
        response = requests.get(url, stream=True)

        if response.status_code == 200:
            with open(file_path, "wb") as output_file:
                output_file.write(response.content)


def extract_data(
    active_datetime: datetime,
):
    if not os.path.exists("./data"):
        os.makedirs("./data")

    _, file_path = get_url_file_path(active_datetime)
    download_data(active_datetime)
    return file_path
