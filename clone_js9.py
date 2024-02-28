from contextlib import closing
from io import BytesIO
from pathlib import Path
import shutil
from sys import prefix
from zipfile import ZipFile

from appdirs import user_data_dir
import requests


print("(clone_js9.py) Downloading JS9 Assets...")
zip_request = requests.get("https://github.com/duytnguyendtn/js9/zipball/jupyterjs9")

def extract_js9(path):
    '''
    param path: The root directory to download JS9 into. Can be string or pathlib.Path object
    '''
    if type(path) is not Path:
        path = Path(path)
    print(f"(clone_js9.py) Attempting to extract JS9 assets to {path}...")
    js9_path = path / "js9"

    # Remove existing install
    if js9_path.exists():
        shutil.rmtree(js9_path)

    # Open the file in memory to avoid disk writing, then extract files from memory directly to disk
    with closing(zip_request), ZipFile(BytesIO(zip_request.content)) as tmpzip:
        tmpzip.extractall(path=path)

    # Rename Github's commit folder to our standard js9 folder
    extracted_repo_folders = [i.name for i in path.iterdir() if i.name.startswith("duytnguyendtn-js9")]
    # There should only be one folder, otherwise, GitHub changed their folder structure and we should stop!
    assert len(extracted_repo_folders) == 1
    (path / extracted_repo_folders[0]).rename(js9_path)


try:
    extract_js9(Path(prefix) / "src")
except PermissionError:
    print(f"(clone_js9.py) Environment extraction failed. Falling back to user data directory.")
    extract_js9(user_data_dir(appname="jupyterjs9", appauthor="heasarc"))
