from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class JobDescription(BaseModel):
    role: str
    required_skills: list[str]
    preferred_skills: list[str]
    minimum_experience: float | None
    education_requirements: list[str]
    responsibilities: list[str]


class MatchResult(BaseModel):
    score: float
    details: dict[str, Any]


class Experience(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    start_date: str | None = None
    role: str | None = None
    duration: str | None = None
    responsibilities: list[str] | None = None
    designation: str | None = None
    description: str | None = None
    skills_used: list[str] | None = None


class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone_number: str | None = None
    linkedin_profile: str | None = None
    career_objective: str | None = None
    education: list[str] | None = None
    skills: list[str] | None = None
    technical_skills: list[str] | None = None
    projects: list[str] | None = None
    certifications: list[str] | None = None
    achievements: list[str] | None = None
    total_experience_years: str | None = None
    experience: list[Experience] | None = None
