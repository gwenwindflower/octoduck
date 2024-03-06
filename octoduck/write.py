import os

import pyarrow as pa
import pyarrow.fs as fs
import pyarrow.parquet as pq
from pyarrow import json

from .schema import pa_schema


def write_data(downloaded_file_path: str, bucket_name: str = "github-events"):
    event_schema = pa.schema(pa_schema)
    parse_options = pa.json.ParseOptions(
        explicit_schema=event_schema, unexpected_field_behavior="ignore"
    )
    table = json.read_json(downloaded_file_path, parse_options=parse_options)
    s3 = fs.FileSystem.from_uri(f"s3://{bucket_name}")
    pq.write_to_dataset(
        table,
        root_path="github-events",
        partition_cols=["year", "month"],
        filesystem=s3,
    )
    os.remove(downloaded_file_path)
