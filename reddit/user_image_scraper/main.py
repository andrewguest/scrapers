from typing import List

import praw

from config import Config
from helpers import download_dir_checker, download_files, clean_duplicates


reddit = praw.Reddit(
    client_id=Config.reddit_client_id,
    client_secret=Config.reddit_client_secret,
    user_agent=Config.reddit_user_agent,
)


def collect_posts(username: str | None) -> List[str] | None:
    """Get the image posts for the given user

    Args:
        username (str | None): Reddit username to scrape

    Returns:
        List[str] | None: List of image URLs
    """
    print(f"Collecting posts with images for: {username}")
    images: List[str] = []

    if username:
        for post in reddit.redditor(username).submissions.new(limit=None):
            # Ignore everything except for .jpg URLs
            if post.url.endswith(".jpg"):
                images.append(post.url)
        print(f"Found {len(images)} image posts for {username}")

    return images


def main():
    download_dir_checker(Config.reddit_username)

    if images_to_download := collect_posts(Config.reddit_username):
        download_files(images_to_download)

    clean_duplicates()


if __name__ == "__main__":
    main()
