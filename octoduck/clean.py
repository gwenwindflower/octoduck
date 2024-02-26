import glob
import os


def clean_data():
    cwd = os.getcwd()
    data_path = f"{cwd}/data/"
    if len(os.listdir(data_path)) == 0:
        print(f"👍 [bold green] No data in {data_path}. Nothing to do![/bold green]")
        return
    json_files = glob.glob(f"{data_path}*.json.gz")
    for file in json_files:
        os.remove(file)
    print(f"🧼 [bold green]Cleaned out {data_path}[/bold green]")
