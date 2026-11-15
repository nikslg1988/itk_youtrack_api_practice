from pydantic import BaseModel, Field


class Project(BaseModel):
    id: str
    name: str


class ProjectSummary(BaseModel):
    name: str


class Issue(BaseModel):
    id: str
    id_readable: str = Field(alias="idReadable")
    summary: str
    project: Project
    description: str | None = None


class IssueItem(BaseModel):
    id: str
    id_readable: str = Field(alias="idReadable")
    summary: str
    project: ProjectSummary
