from __future__ import annotations

from typing import Any


def print_candidate_summary(name: str, score: float, details: dict[str, Any] | None) -> None:
    details = details or {}
    candidate_name = details.get("candidate_name") or details.get("name") or details.get("candidate") or name
    print("\n" + "=" * 70)
    print(f"Candidate: {candidate_name}")
    print(f"Score: {score}%")

    experience_requirement_met = details.get("experience_requirement_met")
    if experience_requirement_met is None:
        experience_requirement_met = details.get("experience_requirement")
    print(f"Experience requirement met: {'Yes' if experience_requirement_met else 'No'}")
    print(f"Overall match percentage: {details.get('overall_match_percentage', score)}%")

    print("\nMatching skills:")
    matching_skills = details.get("matching_skills") or []
    if matching_skills:
        for skill in matching_skills:
            print(f"  - {skill}")
    else:
        print("  - None listed")

    print("\nMissing important skills:")
    missing_skills = details.get("missing_important_skills") or []
    if missing_skills:
        for skill in missing_skills:
            print(f"  - {skill}")
    else:
        print("  - None listed")

    print("\nFinal verdict:")
    verdict = (
        details.get("final_verdict")
        or details.get("verdict")
        or details.get("finalVerdict")
        or "No verdict available"
    )
    print(f"  - {verdict}")
    print("=" * 70)
