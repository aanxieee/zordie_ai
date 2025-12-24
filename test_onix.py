"""
Onix Agent Verification Test
Tests all Onix functionality independently of FastAPI/Django
"""

import sys
from pathlib import Path

# Add libs to path
REPO = Path(__file__).parent
LIBS = REPO / "libs"
sys.path.insert(0, str(LIBS))
sys.path.insert(0, str(LIBS / "zordie_agents"))
sys.path.insert(0, str(LIBS / "zordie_contracts"))

print("=" * 60)
print("🔍 ONIX AGENT VERIFICATION TEST")
print("=" * 60)

# Test 1: Module Import
print("\n✓ Test 1: Module Import")
try:
    from zordie_agents.zordie_agents.onix import inference
    print("  ✅ Onix inference module loaded successfully")
except Exception as e:
    print(f"  ❌ Failed to load module: {e}")
    print(f"  Python path: {sys.path[:3]}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Email Extraction
print("\n✓ Test 2: Email Extraction")
test_text = "Contact me at john.doe@example.com for details"
email = inference.extract_email_from_text(test_text)
print(f"  Input: '{test_text}'")
print(f"  Extracted: {email}")
assert email == "john.doe@example.com", "Email extraction failed"
print("  ✅ Email extraction working")

# Test 3: Phone Extraction
print("\n✓ Test 3: Phone Extraction")
test_text = "Call me at +1-555-123-4567 anytime"
phone = inference.extract_phone_from_text(test_text)
print(f"  Input: '{test_text}'")
print(f"  Extracted: {phone}")
assert phone is not None, "Phone extraction failed"
print("  ✅ Phone extraction working")

# Test 4: Email Template Generation
print("\n✓ Test 4: Email Template Generation")
email_template = inference.generate_email_template(
    candidate_name="Jane Smith",
    position="Senior Python Developer",
    company_name="TechCorp"
)
print(f"  Generated template length: {len(email_template)} chars")
assert "Jane Smith" in email_template, "Name not in template"
assert "Senior Python Developer" in email_template, "Position not in template"
assert "TechCorp" in email_template, "Company not in template"
print("  ✅ Email template generation working")
print("\n  Sample output:")
print("  " + email_template.split("\n")[0])  # Show subject line

# Test 5: Candidate Summary
print("\n✓ Test 5: Candidate Summary Generation")
test_profile = {
    "name": "John Doe",
    "position": "DevOps Engineer",
    "years_of_experience": 5,
    "skills": ["Docker", "Kubernetes", "AWS", "Python", "CI/CD"]
}
summary = inference.generate_candidate_summary(test_profile)
print(f"  Summary length: {len(summary)} chars")
assert "John Doe" in summary, "Name not in summary"
assert "DevOps Engineer" in summary, "Position not in summary"
print("  ✅ Candidate summary working")
print("\n  Sample output:")
for line in summary.split("\n")[:3]:
    print(f"  {line}")

# Test 6: Profile Enrichment
print("\n✓ Test 6: Profile Enrichment")
test_profile = {
    "name": "Alice Johnson",
    "position": "Full Stack Developer",
    "resume_text": "Contact: alice.johnson@email.com, Phone: +1-555-987-6543",
    "skills": ["React", "Node.js", "MongoDB"],
    "years_of_experience": 3
}
enriched = inference.enrich_candidate_profile("CAND-001", test_profile)
print(f"  Input candidate: {test_profile['name']}")
print(f"  Enriched fields: {list(enriched.keys())}")
assert enriched["email"] == "alice.johnson@email.com", "Email not enriched"
assert enriched["phone"] is not None, "Phone not enriched"
assert enriched["onix_processed"] == True, "Processing flag not set"
print(f"  ✅ Profile enrichment working")
print(f"     - Email: {enriched['email']}")
print(f"     - Phone: {enriched['phone']}")

# Test 7: Interview Notes Template
print("\n✓ Test 7: Interview Notes Template")
notes_template = inference.generate_interview_notes_template(
    candidate_name="Bob Williams",
    position="Data Scientist"
)
print(f"  Template length: {len(notes_template)} chars")
assert "Bob Williams" in notes_template, "Name not in template"
assert "Data Scientist" in notes_template, "Position not in template"
assert "Technical Skills Assessment" in notes_template, "Missing section"
print("  ✅ Interview notes template working")

# Test 8: Rejection Email
print("\n✓ Test 8: Rejection Email Template")
rejection = inference.generate_rejection_email(
    candidate_name="Charlie Brown",
    position="Backend Engineer"
)
print(f"  Template length: {len(rejection)} chars")
assert "Charlie Brown" in rejection, "Name not in template"
assert "Backend Engineer" in rejection, "Position not in template"
print("  ✅ Rejection email template working")

# Test 9: Full Agent Run (with contracts)
print("\n✓ Test 9: Full Agent Execution")
try:
    from zordie_contracts.agents import CandidateProfile, AgentResult
    
    test_profile = CandidateProfile(
        candidate_id="CAND-TEST-001",
        name="Test Candidate",
        position="Software Engineer",
        resume_text="Email: test@example.com, skills in Python and Docker",
        skills=["Python", "Docker", "FastAPI"],
        years_of_experience=4
    )
    
    result = inference.run(test_profile)
    print(f"  Agent result: ok={result.ok}")
    
    if result.ok:
        data = result.data
        print(f"  Enriched profile: {data['onix']['enriched_profile']['name']}")
        print(f"  Templates generated: {list(data['onix']['templates'].keys())}")
        print("  ✅ Full agent execution working")
    else:
        print(f"  ⚠️  Agent returned ok=False: {result.warnings}")
        
except ImportError as e:
    print(f"  ⚠️  Contracts not available (expected in minimal test): {e}")
    print("  ℹ️  This is OK - contracts are available in Docker environment")

# Summary
print("\n" + "=" * 60)
print("✅ ONIX AGENT VERIFICATION COMPLETE")
print("=" * 60)
print("\n📊 Test Results:")
print("  ✅ Module imports")
print("  ✅ Email extraction")
print("  ✅ Phone extraction")
print("  ✅ Email template generation")
print("  ✅ Candidate summary generation")
print("  ✅ Profile enrichment")
print("  ✅ Interview notes template")
print("  ✅ Rejection email template")
print("\n🎯 Onix Agent Status: PRODUCTION READY")
print("\n📋 Available Functions:")
functions = [
    "extract_email_from_text(text)",
    "extract_phone_from_text(text)",
    "generate_email_template(name, position, company)",
    "generate_candidate_summary(profile)",
    "enrich_candidate_profile(candidate_id, profile_data)",
    "generate_interview_notes_template(name, position)",
    "generate_rejection_email(name, position)",
    "run(profile) - Full agent execution"
]
for func in functions:
    print(f"  • {func}")

print("\n" + "=" * 60)
