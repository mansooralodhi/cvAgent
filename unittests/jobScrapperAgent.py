
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.jobScraper import JobScraper


def main():
    url = "https://euraxess.ec.europa.eu/jobs/470195"

    scraper = JobScraper()
    job = scraper.scrape(url)

    print("TITLE:")
    print(job.title)

    print("\nJOB DESCRIPTION:")
    print(job.text)


if __name__ == "__main__":
    main()