import glob
import os

import typer
from rich import print

from .extract import extract_data
from .load import load_data

app = typer.Typer()


@app.command()
def extract(start: str = "", end: str = ""):
    extract_data(start, end)


@app.command()
def load():
    load_data()


@app.command()
def prod(start: str = "", end: str = ""):
    extract_data(start, end, prod=True)


@app.command()
def clean():
    cwd = os.getcwd()
    data_path = f"{cwd}/data/"
    if len(os.listdir(data_path)) == 0:
        print(f"👍 [bold green] No data in {data_path}. Nothing to do![/bold green]")
        return
    json_files = glob.glob(f"{data_path}*.json.gz")
    for file in json_files:
        os.remove(file)
    print(f"🧼 [bold green]Cleaned out {data_path}[/bold green]")
