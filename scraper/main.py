import pathlib

import requests
from band import Band
from bs4 import BeautifulSoup

URL = "https://www.metal-archives.com/bands/K.A.IN/3540331289"
PATH = pathlib.Path(__file__).parent
FILENAME = "page.html"


class Scraper:
    def __init__(self, url):
        self.url = url
        self.page = requests.Response()

    def get_page(self):
        self.page = requests.get(self.url, timeout=10)

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
    print(band.to_json())


if __name__ == "__main__":
    main()
