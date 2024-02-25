import os
from datetime import datetime, timedelta

import requests
import typer
from rich import print
from tqdm import tqdm

from .load import load_data

date_format = "%Y-%m-%d-%H"


def validate_to_datetime(date_string: str) -> datetime:
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        print(
            f"[bold red]Invalid date:[/bold red] {date_string}. Please use the format [bold green]YYYY-MM-D-HH[/bold green]"
        )
        raise typer.Abort()


def get_url_file_path(active_datetime):
    url_datetime = datetime.strftime(active_datetime, "%Y-%m-%d-%-H")
    url = f"https://data.gharchive.org/{url_datetime}.json.gz"
    file_path = f"./data/{url_datetime}.json.gz"
    return url, file_path, url_datetime


def download_data(active_datetime):
    # Github Archive URL requires a non-zero-padded hour format
    # ChatGPT tells me '%-H' doesn't work on Windows,
    # but I don't have a Windows machine to test it on so lmk
    url, file_path, url_datetime = get_url_file_path(active_datetime)
    if not os.path.exists(file_path):
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get("content-length", 0))
        progress_bar = tqdm(
            total=total_size_in_bytes,
            unit="kB",
            unit_scale=True,
            leave=False,
            desc=f"💾 Downloading data from Github Archive for {active_datetime}...",
        )

        if response.status_code == 200:
            with open(file_path, "wb") as output_file:
                for chunk in response.iter_content(chunk_size=1024):
                    output_file.write(chunk)
                    progress_bar.update(len(chunk))
            progress_bar.close()
        else:
            print(
                f"💩 [bold red]Crap![/bold red]{url_datetime} returned status code {response.status_code}."
            )
    else:
        print(
            f"🎉 [bold green]Hooray![/bold green] {url_datetime} already exists. Skipping download."
        )


def extract_data(
    start: str = "",
    end: str = "",
    prod: bool = False,
):
    if not os.path.exists("./data"):
        os.makedirs("./data")

    if start == "":
        start = datetime.strftime(datetime.now() - timedelta(hours=3), date_format)
    if end == "":
        end = datetime.strftime(datetime.now() - timedelta(hours=1), date_format)

    start_datetime = validate_to_datetime(start)
    end_datetime = validate_to_datetime(end)

    total_hours = int((end_datetime - start_datetime).total_seconds() / 3600)
    progress_bar = tqdm(total=total_hours)

    active_datetime = start_datetime

    while active_datetime <= end_datetime:
        download_data(active_datetime)
        _, file_path, _ = get_url_file_path(active_datetime)
        active_datetime += timedelta(hours=1)
        progress_bar.update(1)
        if prod:
            load_data(prod=True)
            os.remove(file_path)

    progress_bar.close()
