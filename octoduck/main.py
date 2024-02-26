import os
from datetime import datetime, timedelta

import typer
from rich import print
from rich.progress import Progress

from .clean import clean_data
from .extract import extract_data
from .load import load_data
from .write import write_data

app = typer.Typer()

date_format = "%Y-%m-%d-%H"
extract_description = "💾↓ Downloading files from Github Archive..."
load_description = "🦆🚚 Loading files into DuckDB..."
write_description = "☁️ 📝 Writing to partitioned Parquet in S3..."


def validate_to_datetime(date_string: str) -> datetime:
    try:
        return datetime.strptime(date_string, date_format)
    except ValueError:
        print(
            f"[bold red]Invalid date:[/bold red] {date_string}. Please use the format [bold green]YYYY-MM-D-HH[/bold green]"
        )
        raise typer.Abort()


def get_time_range(start: str, end: str):
    if start == "":
        start = datetime.strftime(datetime.now() - timedelta(hours=3), date_format)
    if end == "":
        end = datetime.strftime(datetime.now() - timedelta(hours=1), date_format)

    start_datetime = validate_to_datetime(start)
    end_datetime = validate_to_datetime(end)
    active_datetime = start_datetime

    total_files = int((end_datetime - start_datetime).total_seconds() / 3600)

    return active_datetime, end_datetime, total_files


@app.command()
def extract(start: str = "", end: str = ""):
    active_datetime, end_datetime, total_files = get_time_range(start, end)

    with Progress() as progress_bar:
        task_extract = progress_bar.add_task(
            extract_description,
            total=total_files,
        )
        while active_datetime <= end_datetime:
            active_datetime += timedelta(hours=1)
            extract_data(active_datetime)
            progress_bar.update(task_extract, advance=1)


@app.command()
def load():
    cwd = os.getcwd()
    data_path = f"{cwd}/data/"
    db_file_path = typer.prompt("❓Where do you want your db file built?", ".")

    total_files = len(os.listdir(data_path))
    with Progress() as progress_bar:
        task_load = progress_bar.add_task(
            load_description,
            total=total_files,
        )
        for file in os.listdir(data_path):
            if file.endswith(".json.gz"):
                file_path = f"{data_path}{file}"
                load_data(db_file_path, file_path)
                progress_bar.update(task_load, advance=1)


@app.command()
def prod(start: str = "", end: str = ""):

    db_file_path = typer.prompt("❓Where do you want your db file built?", ".")
    bucket_name = typer.prompt("❓What is your S3 bucket named?", "github-events")

    active_datetime, end_datetime, total_files = get_time_range(start, end)

    with Progress() as progress_bar:
        task_extract = progress_bar.add_task(
            extract_description,
            total=total_files,
        )
        task_load = progress_bar.add_task(
            load_description,
            total=total_files,
        )
        task_write = progress_bar.add_task(
            write_description,
            total=total_files,
        )
        while active_datetime <= end_datetime:
            # extract
            downloaded_file_path = extract_data(active_datetime)
            progress_bar.update(task_extract, advance=1)

            # load
            load_data(db_file_path, downloaded_file_path)
            progress_bar.update(task_load, advance=1)
            os.remove(downloaded_file_path)

            # write
            write_data(db_file_path, bucket_name)
            progress_bar.update(task_write, advance=1)

            active_datetime += timedelta(hours=1)


@app.command()
def clean():
    clean_data()
