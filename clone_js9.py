from contextlib import closing
from io import BytesIO
from os import environ
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

    # Open the file in memory to avoid disk writing,
    # then extract files from memory directly to disk
    with closing(zip_request), ZipFile(BytesIO(zip_request.content)) as tmpzip:
        tmpzip.extractall(path=path)

    # Rename Github's commit folder to our standard js9 folder
    extracted_repo_folders = [i.name for i in path.iterdir() if i.name.startswith("duytnguyendtn-js9")]
    # There should only be one folder,
    # otherwise GitHub changed their folder structure and we should stop!
    assert len(extracted_repo_folders) == 1
    (path / extracted_repo_folders[0]).rename(js9_path)
    # Verify folder exists:
    assert js9_path.exists()
    print(f"(clone_js9.py) Successfully extracted JS9 to: {js9_path}")


# If the environment variable override INSTALL_JS9 is set to FALSE, skip downloading JS9.
# Using (now deprecated) distutils.util.strtobool definition of FALSE
# https://github.com/python/cpython/blob/v3.11.2/Lib/distutils/util.py#L318
INSTALL_JS9 = str(environ.get("INSTALL_JS9")).lower()
if INSTALL_JS9 in ('n', 'no', 'f', 'false', 'off', '0'):
    dirs_to_try = []
elif INSTALL_JS9 == "user":
    dirs_to_try = [Path(user_data_dir(appname="jupyterjs9", appauthor="heasarc"))]
else:
    dirs_to_try = [Path(prefix) / "src", Path(user_data_dir(appname="jupyterjs9", appauthor="heasarc"))]

for index, dir in enumerate(dirs_to_try):
    try:
        extract_js9(dir)
        break
    except PermissionError as e:
        # If we aren't on the last attempt, allow to fail and try the next one
        if (dirs_to_try.index(dir) + 1) < len(dirs_to_try):
            print(f"(clone_js9.py) Unable to write to {dir}: {e}. Trying next option...")
        # If this is the last attempt, raise the error
        else:
            raise e
