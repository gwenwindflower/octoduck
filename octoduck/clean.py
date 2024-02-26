import glob
import os

from rich import print


def clean_data():
    cwd = os.getcwd()
    data_path = f"{cwd}/data/"
    if len(os.listdir(data_path)) == 0:
        print(
            f"👍 [bold green]No data[/bold green] in {data_path}. [bold green]Nothing to do![/bold green]"
        )
        return
    json_files = glob.glob(f"{data_path}*.json.gz")
    for file in json_files:
        os.remove(file)
    print(f"🧼 [bold green]Cleaned out[/bold green] {data_path}")
