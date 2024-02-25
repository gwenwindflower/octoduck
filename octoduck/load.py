import os

import duckdb
import typer
from rich.progress import track

from .schema import columns, columns_def

app = typer.Typer()


def load_data(prod: bool = False):
    cwd = os.getcwd()
    data_path = f"{cwd}/data/"
    db_file_path = typer.prompt("❓Where do you want your db file built?")

    if prod:
        # You must have a MOTHERDUCK_TOKEN environment variable set for this to work
        connection = "md:"
        # s3
    else:
        connection = f"{db_file_path}/octocatalog.db"

    con = duckdb.connect(database=connection, read_only=False)
    con.sql(
        f"""
        create schema if not exists raw; 
        create table if not exists raw.github_events ({columns_def});
        """
    )
    for file in track(
        os.listdir(data_path), description="🦆 Loading data into DuckDB..."
    ):
        if file.endswith(".json.gz"):
            con.sql(
                f"""
                insert or ignore into raw.github_events 
                select
                    *,
                    date_part('year', created_at) as event_at_year,
                    date_part('month', created_at) as event_at_month,
                from read_json(
                    '{data_path}{file}',
                    columns = {columns}
                );
                """
            )
    if prod:
        con.sql(
            """
            copy raw.github_events 
            to github_events 
            (
                format parquet, partition by (
                    event_at_year,
                    event_at_month
                )
            );
            """
        )
    con.close()