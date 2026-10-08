
from typing import Optional
from pydantic import BaseModel, Field

class JobRequirements(BaseModel):

    jobTitle: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    summary: str = ""
    requiredSkills: list[str] = Field(default_factory=list)
    preferredSkills: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    domains: list[str] = Field(default_factory=list)
    seniority: Optional[str] = None
    educationRequirements: list[str] = Field(default_factory=list)
    experienceRequirements: list[str] = Field(default_factory=list)
    niceToHave: list[str] = Field(default_factory=list)
    # note: adding the below attribute to schema leads to the error: "Schema is too Complex".
    # keywords: list[str] = Field(default_factory=list)