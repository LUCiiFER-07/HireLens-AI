import argparse
import time
from pathlib import Path

from matcher import print_candidate_summary
from parser import extract_job_description, final_score, parse_resume
from reader import load_job_description, read_resume


def main() -> None:
    parser = argparse.ArgumentParser(description="Screen resumes against a job description using an LLM.")
    parser.add_argument("--job-description", default=None, help="Optional path to a .txt/.pdf/.docx job description file")
    parser.add_argument("--resume-folder", default=None, help="Optional folder containing resume files")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    resume_folder = Path(args.resume_folder).resolve() if args.resume_folder else base_dir / "RESUMES"

    if not resume_folder.exists():
        raise FileNotFoundError(f"Resume folder not found: {resume_folder}")

    job_description_text = load_job_description(args.job_description)
    job = extract_job_description(job_description_text)

    all_results = []
    for file_path in sorted(resume_folder.iterdir()):
        if file_path.suffix.lower() not in [".pdf", ".docx"]:
            continue

        print("\nProcessing:", file_path.name)
        resume_text = read_resume(file_path)
        parsed_resume = parse_resume(resume_text)
        time.sleep(2)
        result = final_score(job, parsed_resume)
        time.sleep(2)
        print(f"Score: {result.score}%")
        all_results.append({
            "name": parsed_resume.name,
            "score": result.score,
            "details": result.details,
        })

    if not all_results:
        print("No resume files found to process.")
        return

    all_results.sort(key=lambda candidate: candidate["score"], reverse=True)

    print("\n" + "#" * 70)
    print("RANKED CANDIDATES")
    for index, candidate in enumerate(all_results, start=1):
        print(f"{index}. {candidate['name']} - {candidate['score']}%")
    print("#" * 70)

    top_candidate = all_results[0]
    worst_candidate = all_results[-1]

    print("\nTOP CANDIDATE")
    print_candidate_summary(top_candidate["name"], top_candidate["score"], top_candidate["details"])

    print("\nLOWEST CANDIDATE")
    print_candidate_summary(worst_candidate["name"], worst_candidate["score"], worst_candidate["details"])


if __name__ == "__main__":
    main()