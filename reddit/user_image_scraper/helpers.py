import hashlib
import os
from typing import List

import requests

from config import Config


def download_dir_checker(username: str | None):
    """Check if a 'downloads/<username>' directory exists and create it if not"""

    if username is not None and not os.path.exists(f"downloads/{username}"):
        print(f"No downloads/{username} folder found. Creating.")
        os.makedirs(f"downloads/{username}")


def download_files(files_to_download: List[str]):
    """Download each file in the provided list

    Args:
        files_to_download (List[str]): List of files to download
    """
    print("Starting download")

    download_folder = f"downloads/{Config.reddit_username}"

    for file in files_to_download:
        filename = file.split("/")[
            3
        ]  # keep only the <filename.jpg> part of the URL

        # If the file already exists, skip it
        if os.path.exists(f"{download_folder}/{filename}"):
            print(f"{filename} already exists. Skipping.")
        else:
            req = requests.get(file)
            if req.status_code:
                with open(f"{download_folder}/{filename}", "wb") as f:
                    f.write(req.content)


def clean_duplicates():
    """Remove duplicate downloaded images based on the MD5 hash of each file"""
    print("Cleaning up duplicate files")
    os.chdir(f"downloads/{Config.reddit_username}")
    current_files = os.listdir()

    unique = []
    for filename in current_files:
        if os.path.isfile(filename):
            filehash = hashlib.md5(open(filename, "rb").read()).hexdigest()
            if filehash not in unique:
                unique.append(filehash)
            else:
                os.remove(filename)
