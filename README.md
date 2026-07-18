# 🤖 HireLens AI
# LLM Resume Screening System

> An AI-powered resume screening and candidate ranking system that uses Large Language Models (LLMs) to extract structured information from job descriptions and resumes, evaluate candidate-job compatibility, and rank applicants based on their overall match score.

## Project Banner

```text
┌────────────────────────────────────┐
            🤖HireLens AI                           
      LLM Resume Screening System      
└────────────────────────────────────┘
```

## Project Overview

Recruiters often spend a significant amount of time manually reviewing resumes to identify candidates who satisfy a role's technical and professional requirements. This process becomes increasingly challenging when hiring for specialized roles or when many applicants apply at once.

The LLM Resume Screening System automates this workflow by using an LLM to understand both the job description and candidate resumes semantically rather than relying only on keyword matching. The system extracts structured information from both documents, validates it using Pydantic models, compares the candidate's qualifications against the job requirements, and generates an overall compatibility score along with a concise recruiter-style verdict.

## Project Objectives

- Automate resume screening using Large Language Models.
- Convert unstructured job descriptions into structured JSON.
- Parse resumes into validated structured data.
- Compare candidate qualifications against job requirements.
- Generate an overall candidate matching score.
- Provide recruiters with a concise hiring summary.
- Rank multiple candidates from best to worst match.

## Why This Project?

Manual resume screening has several limitations:

- It is time-consuming for recruiters.
- It can be inconsistent across candidates.
- It is difficult to read resumes with different formats.
- Traditional ATS systems depend heavily on exact keyword matches.
- Important skills may be missed when wording differs.

This project addresses those challenges by combining LLM-based semantic understanding with structured validation.

## Intended Users

This project is suitable for:

- HR recruiters
- Talent acquisition teams
- Hiring managers
- Recruitment startups
- Students learning LLM application development
- Developers exploring AI-powered automation

## Features

### Job Description Analysis

- Extracts structured information from an unstructured job description.
- Identifies role, required skills, preferred skills, minimum experience, education requirements, and responsibilities.
- Validates the extracted data using a Pydantic schema.

### Resume Parsing

Supports resumes in:

- PDF (.pdf)
- Microsoft Word (.docx)

Automatically extracts:

- Candidate name
- Email address
- Phone number
- LinkedIn profile
- Career objective
- Education
- Technical skills
- General skills
- Projects
- Certifications
- Achievements
- Total experience
- Professional experience
- Internship experience

### Semantic Resume Understanding

The LLM is instructed to understand the meaning of resume content rather than only rely on headings such as Experience or Skills.

### Structured Data Validation

All extracted information is validated using strongly typed Pydantic models before being processed further.

### Candidate Matching

Each parsed resume is compared against the structured job description. The evaluation includes:

- Matching skills
- Missing skills
- Experience evaluation
- Overall match percentage
- Final verdict

### Candidate Ranking

After evaluating all resumes, the system sorts candidates by score and prints a ranked summary.

### Multiple Resume Processing

The application scans the RESUMES directory and processes every supported resume file.

## Workflow

```text
Recruiter / Job Description
            │
            ▼
LLM extracts structured requirements
            │
            ▼
Pydantic validation
            │
            ▼
Resume files (PDF / DOCX)
            │
            ▼
Resume text extraction
            │
            ▼
LLM resume parsing engine
            │
            ▼
Structured resume JSON
            │
            ▼
Candidate vs job matching
            │
            ▼
Score + verdict + ranking
```

## Project Architecture

The application is organized into several logical components:

| Module | Responsibility |
|---|---|
| [Resume_parser.py](Resume_parser.py) | Main entry point that orchestrates the full workflow. |
| [models.py](models.py) | Defines the Pydantic schemas for jobs, resumes, experience, and match results. |
| [reader.py](reader.py) | Reads job descriptions and resumes from text, PDF, or DOCX files. |
| [parser.py](parser.py) | Sends prompts to the Groq-backed LLM and validates the structured responses. |
| [matcher.py](matcher.py) | Formats and prints the final ranking summaries. |
| [job_description.txt](job_description.txt) | Stores the default external job description. |

## Architecture Diagram

See [architecture_diagram.md](architecture_diagram.md).

## Workflow Diagram

See [workflow_diagram.md](workflow_diagram.md).

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application language |
| Groq API | LLM access for parsing and scoring |
| GPT-OSS-120B | Model used for structured extraction and matching |
| Pydantic | Schema definition and validation |
| python-dotenv | Loads environment variables securely |
| PyPDF | Extracts text from PDF resumes |
| python-docx | Reads Microsoft Word resumes |
| JSON | Stores structured outputs from the LLM |
| Pathlib | Handles file and directory operations |

## Installation

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd week1/day5
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a file named `.env` and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

### 5. Add resume files

Place candidate resumes inside the RESUMES folder.

Supported formats:

- .pdf
- .docx

## Run the Application

From the project folder, run:

```bash
python main.py
```

You can also point the workflow to a different job description file:

```bash
python Resume_parser.py --job-description job_description.txt --resume-folder RESUMES
```

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| GROQ_API_KEY | API key used to authenticate with the Groq API | Yes |

## Folder Structure

```text
week1/day5/
├── Resume_parser.py
├── main.py
├── models.py
├── reader.py
├── parser.py
├── matcher.py
├── job_description.txt
├── requirements.txt
├── README.md
├── architecture_diagram.md
├── workflow_diagram.md
├── banner.txt
├── sample_output.txt
├── RESUMES/
└── screenshots/
```

## Code Workflow

### read_pdf(file_path)

Reads text from a PDF resume by opening the file with PyPDF and extracting each page's content.

### read_docx(file_path)

Reads text from a Word resume by extracting paragraph and table content through python-docx.

### read_resume(file_path)

Chooses the correct reader based on the file extension.

### parse_resume(resume_text)

Sends the resume content to the LLM to extract structured information into the Resume schema.

### final_score(job, resume)

Compares the job description and parsed resume to produce a match score and detailed verdict.

## Data Models

### JobDescription

Represents the structured job requirements extracted from the job description.

| Field | Description |
|---|---|
| role | Job title |
| required_skills | Mandatory technical skills |
| preferred_skills | Desirable skills |
| minimum_experience | Minimum years of experience |
| education_requirements | Required qualifications |
| responsibilities | Main responsibilities |

### Experience

Represents one professional experience or internship entry.

### Resume

Represents the complete structured resume.

### MatchResult

Represents the final evaluation generated by the LLM.

## LLM Prompts

The project relies on prompt engineering to keep outputs structured and consistent.

- The system prompt instructs the model to act like a recruiter or resume parser.
- The user prompt provides the actual job description or resume text.
- Every request uses JSON-only responses so the output can be validated with Pydantic.

## Matching Process

The matching engine evaluates each candidate by comparing the structured resume data against the structured job description. The LLM is prompted to provide:

- Matching skills
- Missing important skills
- Whether experience requirements are met
- Overall match percentage
- Final verdict

## Candidate Ranking

After all resumes are processed, the application sorts the results in descending order by score and prints both the highest- and lowest-ranked candidates.

## Example Output

See [sample_output.txt](sample_output.txt) for an example of the terminal output.

## Requirements

The project depends on the following packages:

```text
groq
python-dotenv
pydantic
pypdf
python-docx
```

These are listed in [requirements.txt](requirements.txt).

## Future Improvements

Possible next steps include:

- A Streamlit or FastAPI-based user interface
- OCR support for scanned PDFs
- Parallel resume processing
- Retry logic for API rate limits
- Database storage for candidate history
- Unit and integration testing

## Known Limitations

- Supports only PDF and DOCX resumes.
- Requires a valid Groq API key.
- Results depend on LLM responses, which may vary slightly.
- The workflow is terminal-based and does not yet include a GUI.

## Contributing

Contributions are welcome. If you would like to improve the project:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Open a pull request.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Author

Pranjal Bhardwaj

## Acknowledgements

This project makes use of open-source tools such as Python, Groq, Pydantic, PyPDF, python-docx, and python-dotenv.

## Support

If you found this project useful, feel free to share it or extend it further for your own recruitment workflow.
