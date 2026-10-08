
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from agents.cvManager import CVManager
from agents.jobAnalyzer import JobAnalyzer
from agents.jobScraper import JobScraper
from agents.latexEditor import LatexEditor

def main():
    job_url = "https://euraxess.ec.europa.eu/jobs/470246"

    scraper = JobScraper()
    analyzer = JobAnalyzer(model="claude-opus-5-5")
    manager = CVManager(
        knowledge_dir="data/knowledge",
        model="claude-opus-5-5")
    
    job = scraper.scrape(job_url)
    job_requirements = analyzer.analyze_job(job.text)
    tailoring = manager.tailor_cv(job_requirements)
    application_dir = "data/applications/euraxess_470246/cv"

    # LatexEditor use the existing template to generate tailored CV
    editor = LatexEditor(
        master_cv_dir="data/masterCV", 
        output_dir=application_dir,
    )

    main_tex = editor.generate(tailoring)

    print(f"Generated CV: {main_tex}")
    
    print(tailoring.model_dump_json(indent=2))


if __name__ == "__main__":
    main()