import yaml
from pathlib import Path


class KnowledgeLoader:
    def __init__(self, knowledge_dir: str):
        self.knowledge_dir = Path(knowledge_dir)

    def load_all(self) -> dict:
        knowledge = {}

        for file_path in sorted(self.knowledge_dir.glob("*.yaml")):
            with file_path.open("r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or {}

            knowledge.update(data)

        return knowledge

if __name__ == "__main__":
    import os, sys, pathlib
    dir = pathlib.Path.cwd().as_posix() +  '/data/knowledge/'
    print(dir)
    loader = KnowledgeLoader(knowledge_dir=dir)
    knowledge = loader.load_all()
    print(knowledge)