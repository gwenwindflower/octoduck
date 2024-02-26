import duckdb


def write_data(db_file_path: str = ".", bucket_name: str = "github-events"):
    connection = f"{db_file_path}/octocatalog.db"

    con = duckdb.connect(database=connection, read_only=False)
    con.sql(
        f"""
        install aws;
        install httpfs;
        load aws;
        load httpfs;
        call load_aws_credentials('default');
        copy raw.github_events
        to 's3://{bucket_name}'
        (
            format parquet,
            partition_by (
                event_at_year,
                event_at_month
            ),
            overwrite_or_ignore,
            FILENAME_PATTERN \"data_{{i}}\"
        );
        """
    )
    con.close()
