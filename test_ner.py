#!/usr/bin/env python
"""Test NER skills extraction"""

from app.ner_extractor import extract_skills_ner
from app.skills_extractor import extract_skills_hybrid

# Sample resume text
sample_resume = """
Senior Full Stack Developer with 5+ years of experience.

EXPERIENCE:
- Lead Python developer for 3 years at TechCorp
- Developed React applications for 4 years
- Expert in machine learning with TensorFlow and PyTorch

TECHNICAL SKILLS:
- Languages: Python, JavaScript, Java
- Frameworks: Django, Express.js, Spring Boot
- Databases: PostgreSQL, MongoDB, Redis
- Cloud: AWS, Google Cloud Platform
- DevOps: Docker, Kubernetes, GitHub Actions

EDUCATION:
- Bachelor's in Computer Science
- Familiar with data science concepts using pandas and scikit-learn
"""

print("=" * 70)
print("TESTING NER-BASED SKILLS EXTRACTION")
print("=" * 70)

# Test 1: Direct NER extraction
print("\n[TEST 1] Direct NER Extraction:")
print("-" * 70)
try:
    ner_skills = extract_skills_ner(sample_resume)
    print(f"Found {len(ner_skills)} skills via NER:")
    for skill in ner_skills[:10]:  # Show first 10
        print(f"  - {skill.skill_name:20} | Category: {skill.category:20} | "
              f"Confidence: {skill.confidence:.2f} | Proficiency: {skill.proficiency:12} | "
              f"Years: {skill.years_experience}")
    if len(ner_skills) > 10:
        print(f"  ... and {len(ner_skills) - 10} more")
except Exception as e:
    print(f"[ERROR] NER extraction failed: {e}")
    import traceback
    traceback.print_exc()

# Test 2: Hybrid extraction (NER + regex)
print("\n[TEST 2] Hybrid Extraction (NER + Regex):")
print("-" * 70)
try:
    hybrid_skills = extract_skills_hybrid(sample_resume)
    total_skills = sum(len(skills) for skills in hybrid_skills.values())
    print(f"Found {total_skills} skills via hybrid extraction")
    print("\nSkills by category:")
    for category, skills in hybrid_skills.items():
        if skills:
            print(f"\n  {category.upper()} ({len(skills)}):")
            for skill in skills[:5]:  # Show first 5 per category
                print(f"    - {skill.skill_name:20} | Confidence: {skill.confidence:.2f} | "
                      f"Method: {skill.extraction_method:6} | Years: {skill.years_experience}")
            if len(skills) > 5:
                print(f"    ... and {len(skills) - 5} more")
except Exception as e:
    print(f"[ERROR] Hybrid extraction failed: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Proficiency and seniority detection
print("\n[TEST 3] Proficiency and Seniority Detection:")
print("-" * 70)
try:
    hybrid_skills = extract_skills_hybrid(sample_resume)
    print("Top skills by confidence with proficiency and seniority:")
    all_skills = []
    for skills in hybrid_skills.values():
        all_skills.extend(skills)
    all_skills.sort(key=lambda x: x.confidence, reverse=True)

    for skill in all_skills[:15]:
        print(f"  {skill.skill_name:20} | Confidence: {skill.confidence:.2f} | "
              f"Proficiency: {skill.proficiency:12} | Seniority: {skill.seniority_level:6} | "
              f"Years: {skill.years_experience}")
except Exception as e:
    print(f"[ERROR] Proficiency detection failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("NER EXTRACTION TESTS COMPLETED")
print("=" * 70)
