import duckdb
import typer

from .schema import columns, columns_def

app = typer.Typer()


def load_data(db_file_path: str, file_path: str):
    connection = f"{db_file_path}/octocatalog.db"
    con = duckdb.connect(database=connection, read_only=False)
    con.sql(
        f"""
        create schema if not exists raw; 
        create table if not exists raw.github_events ({columns_def});
        """
    )
    con.sql(
        f"""
        insert or ignore into raw.github_events 
        select
            *,
            date_part('year', created_at) as event_at_year,
            date_part('month', created_at) as event_at_month,
        from read_json(
            '{file_path}',
            columns = {columns}
        );
        """
    )
    con.close()
