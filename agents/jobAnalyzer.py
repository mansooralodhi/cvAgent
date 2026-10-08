import os
from pathlib import Path
from dotenv import load_dotenv
from anthropic import Anthropic
from schemas.jobRequirements import JobRequirements

load_dotenv()

class JobAnalyzer:
    def __init__(self, model: str):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY environment variable is not set.")
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def analyze_job(self, job_text: str) -> JobRequirements:
        promptTemplate = Path("prompts/analyzeJob.md").read_text(encoding="utf-8")
        prompt = promptTemplate.format(JOB_TEXT = job_text)

        response = self.client.messages.parse(
                                    model=self.model,
                                    max_tokens=3000,
                                    cache_control={"type": "ephemeral"},
                                    messages=[
                                        {
                                            "role": "user",
                                            "content": prompt,
                                        }],
                                    output_format=JobRequirements)
        return response.parsed_output