from pydantic import BaseModel, Field


class TailoredProject(BaseModel):
    sourceId: str
    include: bool = True
    title: str | None = None
    bullets: list[str] = Field(default_factory=list)
    relevantSkills: list[str] = Field(default_factory=list)
    # matchedRequirements: list[str] = Field(default_factory=list)
    relevanceReason: str = ""

class TailoredExperience(BaseModel):
    sourceId: str
    include: bool = True
    title: str | None = None
    company: str | None = None
    bullets: list[str] = Field(default_factory=list)
    relevantSkills: list[str] = Field(default_factory=list)
    # matchedRequirements: list[str] = Field(default_factory=list)
    relevanceReason: str = ""

class TailoredEducation(BaseModel):
    sourceId: str
    include: bool = True
    degree: str | None = None
    institution: str | None = None
    emphasis: str = ""

class TailoredAward(BaseModel):
    sourceId: str
    include: bool = True
    title: str | None = None
    description: str | None = None

class TailoredPublication(BaseModel):
    sourceId: str
    include: bool = True

class TailoredSkills(BaseModel):
    programmingLanguages: list[str] = Field(default_factory=list)
    databases: list[str] = Field(default_factory=list)
    dataScience: list[str] = Field(default_factory=list)
    machineLearningAi: list[str] = Field(default_factory=list)
    applicationDevelopment: list[str] = Field(default_factory=list)
    toolsPlatforms: list[str] = Field(default_factory=list)

class CVTailoring(BaseModel):
    targetRole: str = ""
    professionalSummary: str | None = None
    education: list[TailoredEducation] = Field(default_factory=list)
    experience: list[TailoredExperience] = Field(default_factory=list)
    projects: list[TailoredProject] = Field(default_factory=list)
    skills: TailoredSkills = Field(default_factory=TailoredSkills)
    awards: list[TailoredAward] = Field(default_factory=list)
    publications: list[TailoredPublication] = Field(default_factory=list)