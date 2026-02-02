"""
Test file for Day 1 (Parser) and Day 2 (Skills Extraction & Comparison)
"""

from app.parser import extract_text, extract_contact_info
from app.skills_extractor import extract_skills, extract_skills_as_set
from app.scoring import compare_skills, compare_skills_from_text, get_skills_by_category


def test_day1_parser():
    print("\n" + "="*70)
    print("TEST - DAY 1: Document Parsing & Contact Extraction")
    print("="*70)
    
    file_path = "C:\\Users\\asyed\\coding\\resume scanner\\data\\sample.pdf"
    
    try:
        resume_text = extract_text(file_path)
        contact_info = extract_contact_info(resume_text)
        
        print("\n✓ Document parsed successfully")
        print("\n=== CONTACT INFORMATION ===")
        print(f"Email(s): {contact_info['email']}")
        print(f"Phone(s): {contact_info['phone']}")
        print(f"LinkedIn: {contact_info['linkedin']}")
        print(f"GitHub: {contact_info['github']}")
        
        return resume_text
    
    except FileNotFoundError:
        print(f"⚠️  Sample file not found at {file_path}")
        print("   Using sample text for demo instead...")
        return None


def test_skills_extraction():
    print("\n" + "="*70)
    print("TEST 1: Skills Extraction from Text")
    print("="*70)
    
    sample_text = """
    I'm a software developer with 5 years of experience in Python, JavaScript, 
    and TypeScript. I have worked extensively with React and Node.js to build 
    web applications. My backend experience includes Django, FastAPI, and Express.js.
    
    I'm proficient with PostgreSQL and MongoDB for database management, and I've 
    deployed applications on AWS and GCP. I use Docker and Kubernetes for 
    containerization and microservices architecture.
    
    I'm familiar with REST APIs, GraphQL, and WebSockets. I also have experience 
    with CI/CD pipelines using GitHub Actions and Jenkins.
    """
    
    skills = extract_skills(sample_text)
    
    print("\n✓ Extracted Skills by Category:")
    for category, skill_list in skills.items():
        if skill_list:
            print(f"\n  {category.replace('_', ' ').title()}:")
            for skill in skill_list:
                print(f"    - {skill}")
    
    print(f"\n✓ Total unique skills found: {sum(len(v) for v in skills.values())}")
    return skills


def test_job_description_parsing():
    """Test extracting skills from job description"""
    print("\n" + "="*70)
    print("TEST 2: Skills Extraction from Job Description")
    print("="*70)
    
    # Read the sample job description
    try:
        with open('data/sample_job_description.txt', 'r') as f:
            job_text = f.read()
    except FileNotFoundError:
        print("❌ Job description file not found at data/sample_job_description.txt")
        return None
    
    print("\n📋 Job Description Excerpt:")
    print(job_text[:300] + "...\n")
    
    job_skills = extract_skills(job_text)
    
    print("✓ Extracted Job Requirements by Category:")
    for category, skill_list in job_skills.items():
        if skill_list:
            print(f"\n  {category.replace('_', ' ').title()}:")
            for skill in skill_list:
                print(f"    - {skill}")
    
    print(f"\n✓ Total unique skills required: {sum(len(v) for v in job_skills.values())}")
    return job_skills


def test_skills_comparison():
    """Test comparing resume skills with job requirements"""
    print("\n" + "="*70)
    print("TEST 3: Skills Comparison (Set Operations)")
    print("="*70)
    
    # Sample resume text
    resume_text = """
    Senior Python Developer with 6 years of experience.
    
    Technical Skills:
    - Languages: Python, JavaScript, SQL
    - Frameworks: Django, FastAPI, React, Express.js
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS, GCP
    - DevOps: Docker, GitHub Actions
    - APIs: REST API, GraphQL
    
    Experience:
    Developed microservices using Python and FastAPI. Deployed applications 
    on AWS using Docker containers. Implemented CI/CD pipelines with GitHub 
    Actions.
    """
    
    # Read job description
    try:
        with open('data/sample_job_description.txt', 'r') as f:
            job_text = f.read()
    except FileNotFoundError:
        print("❌ Job description file not found")
        return None
    
    print("\n📝 Comparing Resume vs Job Requirements...\n")
    
    # Get skills as sets for comparison
    resume_skills = extract_skills_as_set(resume_text)
    job_skills = extract_skills_as_set(job_text)
    
    print(f"Resume skills count: {len(resume_skills)}")
    print(f"Job skills count: {len(job_skills)}")
    
    # Compare skills
    comparison = compare_skills(resume_skills, job_skills)
    
    print("\n" + "-"*70)
    print("COMPARISON RESULTS")
    print("-"*70)
    
    # Matching skills
    print(f"\n✅ MATCHING SKILLS ({comparison['matching_count']}):")
    if comparison['matching']:
        for skill in comparison['matching']:
            print(f"   ✓ {skill}")
    else:
        print("   (none)")
    
    # Missing skills
    print(f"\n❌ MISSING SKILLS ({comparison['missing_count']}):")
    if comparison['missing']:
        for skill in comparison['missing']:
            print(f"   ✗ {skill}")
    else:
        print("   (none - perfect match!)")
    
    # Additional skills
    print(f"\n⭐ ADDITIONAL SKILLS ({comparison['additional_count']}):")
    if comparison['additional']:
        for skill in comparison['additional'][:5]:  # Show first 5
            print(f"   + {skill}")
        if len(comparison['additional']) > 5:
            print(f"   + ... and {len(comparison['additional']) - 5} more")
    else:
        print("   (none)")
    
    # Match percentage
    print(f"\n📊 MATCH SCORE: {comparison['match_percentage']}%")
    print(f"   ({comparison['matching_count']}/{comparison['total_job_skills']} required skills match)")
    
    return comparison


def test_skills_by_category():
    """Test detailed comparison organized by category"""
    print("\n" + "="*70)
    print("TEST 4: Detailed Category Breakdown")
    print("="*70)
    
    resume_text = """
    Python and JavaScript developer experienced with React, Django, and AWS.
    I use PostgreSQL and Redis. I'm comfortable with Docker and Kubernetes.
    """
    
    try:
        with open('data/sample_job_description.txt', 'r') as f:
            job_text = f.read()
    except FileNotFoundError:
        print("❌ Job description file not found")
        return None
    
    category_breakdown = get_skills_by_category(resume_text, job_text)
    
    print("\n📋 Skills Breakdown by Category:\n")
    
    for category, details in category_breakdown.items():
        if details['job_skills']:  # Only show categories with job requirements
            print(f"\n{category.replace('_', ' ').upper()}")
            print("-" * 50)
            
            print(f"  Resume: {', '.join(details['resume_skills']) if details['resume_skills'] else '(none)'}")
            print(f"  Job Requires: {', '.join(details['job_skills'])}")
            
            if details['matching']:
                print(f"  ✓ Match: {', '.join(details['matching'])}")
            
            if details['missing']:
                print(f"  ✗ Missing: {', '.join(details['missing'])}")


def main():
    """Run all tests"""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  RESUME SCANNER - TEST SUITE (DAY 1 & 2)  ".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    try:
        # Run tests
        test_day1_parser()
        test_skills_extraction()
        test_job_description_parsing()
        test_skills_comparison()
        test_skills_by_category()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
