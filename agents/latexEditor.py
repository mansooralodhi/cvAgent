from pathlib import Path
import shutil


class LatexEditor:
    def __init__(self, master_cv_dir: str, output_dir: str):
        self.master_cv_dir = Path(master_cv_dir)
        self.output_dir = Path(output_dir)

    def generate(self, customization) -> Path:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._copy_static_files()

        self._write_education(customization.education)
        self._write_experience(customization.experience)
        self._write_projects(customization.projects)
        self._write_skills(customization.skills)
        self._write_awards(customization.awards)
        self._write_publications(customization.publications)

        return self.output_dir / "main.tex"

    def _copy_static_files(self) -> None:
        for filename in ["main.tex", "_preamble.tex", "_template.tex"]:
            shutil.copy2(
                self.master_cv_dir / filename,
                self.output_dir / filename,
            )

    def _write_education(self, education) -> None:
        lines = [
            "%-----------EDUCATION-----------",
            "\\section{Education}",
            "  \\resumeSubHeadingListStart",
        ]

        for item in education:
            if not item.include:
                continue

            lines.extend([
                "    \\resumeSubheading",
                f"      {{{self._escape(item.institution)}}}{{}}",
                f"      {{{self._escape(item.degree)}}}{{}}",
                "      {}{}",
            ])

        lines.append("  \\resumeSubHeadingListEnd")

        self._write_file("education.tex", lines)

    def _write_experience(self, experience) -> None:
        lines = [
            "%-----------EXPERIENCE-----------",
            "\\section{Experience}",
            "  \\resumeSubHeadingListStart",
        ]

        for item in experience:
            if not item.include:
                continue

            lines.extend([
                "    \\resumeSubheading",
                f"      {{{self._escape(item.title or '')}}}{{}}",
                f"      {{{self._escape(item.company or '')}}}{{}}",
                "      \\resumeItemListStart",
            ])

            for bullet in item.bullets:
                lines.append(
                    f"        \\resumeItem{{{self._escape(bullet)}}}"
                )

            lines.extend([
                "      \\resumeItemListEnd",
            ])

        lines.append("  \\resumeSubHeadingListEnd")

        self._write_file("experience.tex", lines)

    def _write_projects(self, projects) -> None:
        lines = [
            "%-----------PROJECTS-----------",
            "\\section{Academic Projects}",
            "    \\resumeSubHeadingListStart",
        ]

        for item in projects:
            if not item.include:
                continue

            title = item.title or ""

            lines.extend([
                "      \\resumeProjectHeading",
                f"          {{\\textbf{{{self._escape(title)}}}}}{{}}",
                "          \\resumeItemListStart",
            ])

            for bullet in item.bullets:
                lines.append(
                    f"            \\resumeItem{{{self._escape(bullet)}}}"
                )

            lines.extend([
                "          \\resumeItemListEnd",
            ])

        lines.extend([
            "    \\resumeSubHeadingListEnd",
        ])

        self._write_file("projects.tex", lines)

    def _write_skills(self, skills) -> None:
        lines = [
            "\\section{Technical Skills}",
            "\\begin{itemize}[leftmargin=0.15in, label={}]",
            "    \\small",
        ]

        categories = [
            ("Programming Languages", skills.programmingLanguages),
            ("Databases", skills.databases),
            ("Data Science", skills.dataScience),
            ("Machine Learning \\& AI", skills.machineLearningAi),
            ("Application Development", skills.applicationDevelopment),
            ("Tools \\& Platforms", skills.toolsPlatforms),
        ]

        for name, values in categories:
            if not values:
                continue

            skill_text = ", ".join(
                self._escape(value) for value in values
            )

            lines.append(
                f"    \\item \\textbf{{{name}:}} "
                f"{skill_text} \\vspace{{-1ex}}\\\\"
            )

        lines.append("\\end{itemize}")

        self._write_file("skills.tex", lines)

    def _write_awards(self, awards) -> None:
        lines = [
            "\\section{Awards}",
            "\\vspace{-1ex}",
            "    \\resumeSubHeadingListStart",
        ]

        for item in awards:
            if not item.include:
                continue

            lines.extend([
                "      \\resumeProjectHeading",
                f"      {{\\textbf{{{self._escape(item.title or '')}}}}}{{}}",
            ])

            if item.description:
                lines.append(
                    f"      {{}}{{{self._escape(item.description)}}}"
                )

        lines.append("    \\resumeSubHeadingListEnd")

        self._write_file("awards.tex", lines)

    def _write_publications(self, publications) -> None:
        # First version: preserve the master publication component.
        # Publication customization can be implemented later.
        source = self.master_cv_dir / "publication.tex"
        destination = self.output_dir / "publication.tex"

        shutil.copy2(source, destination)

    def _write_file(self, filename: str, lines: list[str]) -> None:
        path = self.output_dir / filename

        path.write_text(
            "\n".join(lines) + "\n",
            encoding="utf-8",
        )

    @staticmethod
    def _escape(value: str) -> str:
        replacements = {
            "&": "\\&",
            "%": "\\%",
            "$": "\\$",
            "#": "\\#",
            "_": "\\_",
            "{": "\\{",
            "}": "\\}",
        }

        for old, new in replacements.items():
            value = value.replace(old, new)

        return value