from __future__ import annotations

import json
import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from models import JobDescription, MatchResult, Resume

load_dotenv()

DEFAULT_MODEL = "openai/gpt-oss-120b"


def get_client() -> Groq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GROQ_API_KEY. Set it in your environment or .env before running the parser.")
    return Groq(api_key=api_key)


def _extract_structured_data(
    *,
    system_prompt: str,
    user_prompt: str,
    model: str = DEFAULT_MODEL,
) -> dict[str, Any]:
    client = get_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={"type": "json_object"},
    )
    raw_output = response.choices[0].message.content
    return json.loads(raw_output)


def extract_job_description(job_description_text: str) -> JobDescription:
    jobd_schema = JobDescription.model_json_schema()
    system_prompt = f"""
You are a highly skilled recruiter specializing in Instrumentation & Control Engineering.
Return the job description in a structured JSON format that adheres to the following schema:
{jobd_schema}

IMPORTANT:
Do NOT return the schema itself.
Do NOT return fields like "properties", "type", "title", "description", "required" or other schema metadata.
Fill the schema with the relevant information extracted from the provided job description.
If minimum_experience is not mentioned in the job description, return it as null.
If information is not available for any field, return it as an empty list or null as appropriate.
Do not invent any information that is not present in the job description.
"""
    user_prompt = f"""
Analyse the following job description and extract the relevant information to populate the fields of the schema.

{job_description_text}
"""
    data = _extract_structured_data(system_prompt=system_prompt, user_prompt=user_prompt)
    return JobDescription(**data)


def parse_resume(resume_text: str) -> Resume:
    resume_schema = Resume.model_json_schema()
    system_prompt = f"""
You are an expert resume parser.
Extract information from the resume based on its meaning, not only based on exact headings.
Different resumes may use different headings.

Examples:
- Experience
- Professional Experience
- Work History
- Employment
- Internships

Skills may also appear in the skills section, work experience, internships, or projects.

Return ONLY valid JSON matching this schema:
{resume_schema}

Important Rules:
1. Do not invent information.
2. If a value is not available, return null.
3. If a list has no information, return an empty list.
4. Include internships inside experiences.
5. Extract skills mentioned across the entire resume.
"""
    user_prompt = f"""
Parse the following resume:

{resume_text}
"""
    data = _extract_structured_data(system_prompt=system_prompt, user_prompt=user_prompt)
    return Resume(**data)


def final_score(job: JobDescription, resume: Resume) -> MatchResult:
    match_schema = MatchResult.model_json_schema()
    prompt = f"""
You are an HR recruiter.
Compare the candidate's resume with the job description.

JOB DESCRIPTION:
{job.model_dump_json(indent=2)}

CANDIDATE RESUME:
{resume.model_dump_json(indent=2)}

Return JSON matching this schema:
{match_schema}

Give me:
1. Candidate name
2. Matching skills
3. Missing important skills
4. Whether experience requirement is met
5. Overall match percentage from 0 to 100
6. A short final verdict

Keep the response concise and easy to read.
"""
    client = get_client()
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
    )
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    return MatchResult(**data)
