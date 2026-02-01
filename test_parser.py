from app.parser import extract_text, extract_contact_info

file_path = "C:\\Users\\asyed\\coding\\resume scanner\\data\\sample.pdf"
resume_text = extract_text(file_path)

contact_info = extract_contact_info(resume_text)

print("\n=== CONTACT INFORMATION ===")
print(f"Email(s): {contact_info['email']}")
print(f"Phone(s): {contact_info['phone']}")
print(f"LinkedIn: {contact_info['linkedin']}")
print(f"GitHub: {contact_info['github']}")
