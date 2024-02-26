import typer

from .clean import clean_data
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
    clean_data()
