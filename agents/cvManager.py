
import os
import json
from pathlib import Path
from anthropic import Anthropic

from schemas.tailoredCV import CVTailoring
from schemas.jobRequirements import JobRequirements
from utils.knowledgeLoader import KnowledgeLoader


class CVManager:
    def __init__(self, knowledge_dir: str, model: str):
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set.")
        self.model = model
        self.client = Anthropic(api_key=api_key)
        self.knowledge_loader = KnowledgeLoader(knowledge_dir)

    def tailor_cv(self, job_requirements: JobRequirements) -> CVTailoring:
        knowledge = self.knowledge_loader.load_all()
        prompt = self._build_prompt(knowledge, job_requirements)
        response = self.client.messages.create(
                                model=self.model,
                                max_tokens=6000,
                                messages=[{
                                        "role": "user",
                                        "content": prompt}])
        response_text = self._extract_text(response)
        data = self._parse_json(response_text)
        
        tailoring = CVTailoring.model_validate(data)
        self._validate_source_ids(tailoring, knowledge)
        # self._validate_requirement_coverage(tailoring, job_requirements)
        return tailoring

    def _build_prompt(self, knowledge: dict, job_requirements: JobRequirements) -> str:
        schema = CVTailoring.model_json_schema()
        promptTemplate = Path("prompts/tailorCV.md").read_text(encoding="utf-8")
        return promptTemplate.format(
            JOB_REQUIREMENTS = json.dumps(
                                    job_requirements.model_dump(),
                                    indent=2,
                                    ensure_ascii=False),
            CANDIDATE_KNOWLEDGE = json.dumps(
                                    knowledge,
                                    indent=2,
                                    ensure_ascii=False),
            SCHEMA = json.dumps(schema, indent=2))    

    def _extract_text(self, response) -> str:
        text_parts = []

        for block in response.content:
            if getattr(block, "type", None) == "text":
                text_parts.append(block.text)

        if not text_parts:
            raise ValueError("Claude returned no text content.")

        return "\n".join(text_parts)

    def _parse_json(self, response_text: str) -> dict:
        response_text = response_text.strip()
        if response_text.startswith("```"):
            response_text = response_text.replace("```json", "", 1)
            response_text = response_text.replace("```", "", 1)
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError as exc:
            raise ValueError(
                "Claude returned invalid JSON."
            ) from exc

    def _validate_source_ids(
            
        self, tailoring: CVTailoring, knowledge: dict) -> None:
        experience_ids = {
            item["id"]
            for item in knowledge.get("experience", [])}
        project_ids = {
            item["id"]
            for item in knowledge.get("projects", [])}
        education_ids = {
            item["id"]
            for item in knowledge.get("education", [])}
        award_ids = {
            item["id"]
            for item in knowledge.get("awards", [])}
        publication_ids = {
            item["id"]
            for item in knowledge.get("publications", [])}
        for item in tailoring.experience:
            if item.sourceId not in experience_ids:
                raise ValueError(
                    f"Unknown experience sourceId: "
                    f"{item.sourceId}")
        for item in tailoring.projects:
            if item.sourceId not in project_ids:
                raise ValueError(
                    f"Unknown project sourceId: "
                    f"{item.sourceId}")
        for item in tailoring.education:
            if item.sourceId not in education_ids:
                raise ValueError(
                    f"Unknown education sourceId: "
                    f"{item.sourceId}")
        for item in tailoring.awards:
            if item.sourceId not in award_ids:
                raise ValueError(
                    f"Unknown award sourceId: "
                    f"{item.sourceId}")
        for item in tailoring.publications:
            if item.sourceId not in publication_ids:
                raise ValueError(
                    f"Unknown publication sourceId: "
                    f"{item.sourceId}")
            
    def _validate_requirement_coverage(self, tailoring: CVTailoring,
        job_requirements: JobRequirements) -> None:
        required_requirements = set(job_requirements.requiredSkills)
        covered_requirements = set()
        for experience in tailoring.experience:
            if experience.include:
                covered_requirements.update(experience.matchedRequirements)
        for project in tailoring.projects:
            if project.include:
                covered_requirements.update(project.matchedRequirements)
        uncovered_requirements = (required_requirements - covered_requirements)
        if uncovered_requirements:
            print("Warning: uncovered required skills:")
            for requirement in sorted(uncovered_requirements):
                print(f"  - {requirement}")