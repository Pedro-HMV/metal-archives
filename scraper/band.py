import json


class Band:
    def __init__(self) -> None:
        self.name: str | None = None
        self.genre: str | None = None
        self.country: str | None = None
        self.location: str | None = None
        self.status: str | None = None
        self.formed_in: str | None = None
        self.years_active: str | None = None
        self.lyrical_themes: str | None = None
        self.years_active: str | None = None
        self.current_label: str | None = None

    def cleanup(self):
        for key, value in self.__dict__.items():
            if isinstance(value, str):
                self.__dict__[key] = value.strip()

    def populate(self, soup):
        self.name = soup.find("h1", class_="band_name").text

        stats = soup.find("div", id="band_stats")
        info = {}
        details = stats.find_all(["dt", "dd"])

        for i in range(0, len(details), 2):
            info[details[i].text] = details[i + 1].text

        self.country = info["Country of origin:"]
        self.genre = info["Genre:"]
        self.location = info["Location:"]
        self.status = info["Status:"]
        self.formed_in = info["Formed in:"]
        self.years_active = info["Years active:"]
        self.lyrical_themes = info["Themes:"]
        self.current_label = info["Current label:"]

    def to_json(self):
        return json.dumps(self.__dict__, indent=4)
