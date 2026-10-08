import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.jobScraper import JobScraper
from agents.jobAnalyzer import JobAnalyzer


def main():
    job_url = "https://euraxess.ec.europa.eu/jobs/470246"

    scraper = JobScraper()
    job = scraper.scrape(job_url)

    analyzer = JobAnalyzer(
        model="claude-opus-5-5"
    )

    requirements = analyzer.analyze_job(job.text)

    print(requirements)
    print(requirements.jobTitle)
    print(requirements.requiredSkills)
    print(requirements.model_dump_json(indent=2))


if __name__ == "__main__":
    main()