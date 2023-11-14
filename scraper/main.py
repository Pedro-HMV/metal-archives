import logging
import os
import pathlib
import time

import requests
from band import Band
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

URL = "https://www.metal-archives.com/bands/K.A.IN/3540331289"
PATH = pathlib.Path(__file__).parent
FILENAME = "page.html"
DEBUG = os.getenv("DEBUG") == "True"


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

log_dir = pathlib.Path(PATH / "logs")
log_dir.mkdir(exist_ok=True)

handler = logging.FileHandler(PATH / log_dir / "scraper.log")
handler.setLevel(logger.level)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logger.level)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)


class Scraper:
    def __init__(self, url):
        self.url = url
        self.page = requests.Response()
        self.logger = logger

    def get_page(self):
        try:
            self.logger.info(f"Starting to scrape URL: {self.url}")
            start_time = time.time()
            self.page = requests.get(self.url, timeout=10)
        except Exception as e:
            self.logger.exception(f"Error scraping URL: {self.url}\n{e}")
            return
        elapsed_time = time.time() - start_time
        self.logger.info(
            f"Finished scraping URL: {self.url} in"
            f" {round(elapsed_time, 2)} seconds"
        )

    def write_file(self) -> None:
        with open(PATH / FILENAME, "w") as f:
            f.write(self.page.text)


def create_page() -> None:
    scraper = Scraper(URL)
    scraper.get_page()
    scraper.write_file()


def create_band() -> Band:
    band = Band()

    with open(PATH / FILENAME, "r") as f:
        page = f.read()

    soup = BeautifulSoup(page, "html.parser")
    band.populate(soup)
    band.cleanup()

    return band


def main():
    create_page()
    band = create_band()
    logger.info(band.to_json())


if __name__ == "__main__":
    main()
