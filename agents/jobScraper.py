from dataclasses import dataclass
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


@dataclass
class scrapedJob:
    url: str
    title: str | None
    text: str


class JobScraper:
    def __init__(self, timeout: int = 20):
        self.timeout = timeout

    def scrape(self, url: str) -> scrapedJob:
        self._validate_url(url)

        response = requests.get(
            url,
            timeout=self.timeout,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/140.0 Safari/537.36"
                )
            },
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        title = self._extract_title(soup)
        text = self._extract_text(soup)

        if not text:
            raise ValueError("No usable text found on the job page.")

        return scrapedJob(
            url=url,
            title=title,
            text=text,
        )

    def _validate_url(self, url: str) -> None:
        parsed_url = urlparse(url)

        if parsed_url.scheme not in {"http", "https"}:
            raise ValueError("Job URL must use HTTP or HTTPS.")

        if not parsed_url.netloc:
            raise ValueError("Invalid job URL.")

    def _extract_title(self, soup: BeautifulSoup) -> str | None:
        if soup.title and soup.title.string:
            return soup.title.string.strip()
        
        heading = soup.find("h1")
        
        if heading:
            return heading.get_text(" ", strip=True)
        
        return None

    def _extract_text(self, soup: BeautifulSoup) -> str:
        for element in soup(
            [
                "script",
                "style",
                "noscript",
                "svg",
                "nav",
                "footer",
                "header",
            ]
        ):
            element.decompose()

        text = soup.get_text(separator="\n")

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        return "\n".join(lines)