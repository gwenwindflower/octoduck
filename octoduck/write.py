import pyarrow.fs as fs
import pyarrow.parquet as pq
from pyarrow import json


def write_data(downloaded_file_path: str, bucket_name: str = "github-events"):
    table = json.read_json(downloaded_file_path)
    s3 = fs.FileSystem.from_uri(f"s3://{bucket_name}")
    pq.write_to_dataset(
        table,
        root_path="github-events",
        partition_cols=["year", "month"],
        filesystem=s3,
    )
