from docx import Document
import os
import re

# Create a new Document
doc = Document()
folder_path = r"C:/Users/tamme/OneDrive/Desktop/Files/Docs/Job Emails"
files = os.listdir(folder_path)
docx_files = [f for f in files if f.endswith('.docx')]
numbers = [int(re.match(r'(\d+)', f).group(1)) for f in docx_files if re.match(r'(\d+)', f)]
num = max(numbers) + 1 if numbers else 1

# Prompt the user for input
name = input("Recipient's name: ")
interest_sentence = input("Sentence highlighting your interest and connection to the recipient: ")
internship_interest = input("Interest in the internship opportunity: ")
additional_details = input("Additional details to your request: ")

# Fill in the email template
email_content = f"""
Hi {name},

My name is Tammer and I’m an undergraduate at Northeastern University in CS and Econ. {interest_sentence} I’m currently looking for a spring co-op/internship.

I’m reaching out because {internship_interest}. {additional_details}

I’ve attached my resume for your consideration. Please let me know if you have any questions! Thank you so much for your time.

Best,
Tammer Haddad
"""

# Add the email content to the document
doc.add_paragraph(email_content)

# Save the document to the specified path
file_path = rf"C:/Users/tamme/OneDrive/Desktop/Files/Docs/Job Emails/{num}.docx"
doc.save(file_path)