import time
import streamlit as st
from sentence_transformers import SentenceTransformer, util
import PyPDF2
import docx
import requests
import re
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
# Bloom API configuration
API_URL=os.getenv("API_URL")
headers = {"Authorization": os.getenv("headers_value")}
# Pre-trained Sentence Transformer models
models = {
    "paraphrase-MiniLM-L6-v2": "paraphrase-MiniLM-L6-v2",
    "all-mpnet-base-v2": "all-mpnet-base-v2"
}

# Cache for generated email content
email_cache = {}

def extract_email_from_text(text):
    # Use a regular expression to extract email addresses from the text
    email_pattern = r'\S+@\S+'
    email_matches = re.findall(email_pattern, text)
    if email_matches:
        return email_matches[0]
    else:
        return None
def generate_email_with_bloom(candidate_name, candidate_skills):
    # Check if the email content is cached
    if candidate_name in email_cache:
        return email_cache[candidate_name]
    
    # Use the Bloom model to generate a personalized email
    email_content = f"Dear {candidate_name},\nWe are pleased to inform you that your skills in {candidate_skills} align well with the job requirements. We would like to invite you to the next round of interviews."
    
    # Cache the email content
    email_cache[candidate_name] = email_content
    return email_content


# def generate_email(candidate_name, candidate_skills):
#     # Check if the email content is cached
#     if candidate_name in email_cache:
#         return email_cache[candidate_name]
    
#     # Use GPT-3 to generate a personalized email
#     prompt = f"Dear {candidate_name},\n\nWe are pleased to inform you that your skills in {candidate_skills} align well with the job requirements. We would like to invite you to the next round of interviews."
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=100,
#         n=1,
#         stop=None,
#         temperature=0.2
#     )
#     email_content = response.choices[0].text.strip()
    
#     # Cache the email content
#     email_cache[candidate_name] = email_content
#     return email_content

def send_email(api_key, domain, from_email, to_email, subject, email_content):
    # Mailgun API endpoint
    endpoint = f"https://api.mailgun.net/v3/{domain}/messages"

    # Create email data
    email_data = {
        "from": from_email,
        "to": to_email,
        "subject": subject,
        "text": email_content
    }

    # Send email using Mailgun API
    response = requests.post(endpoint, auth=("api", api_key), data=email_data)

    # Check the response status
    if response.status_code == 200:
        return True  # Email sent successfully
    else:
        return False  # Email sending failed
def calculate_similarity(text1, text2, selected_model):
    # Load the selected Sentence Transformer model
    sentence_transformer_model = SentenceTransformer(models[selected_model])
    
    # Use the selected model to calculate the cosine similarity between two texts
    embedding1 = sentence_transformer_model.encode([text1], convert_to_tensor=True)
    embedding2 = sentence_transformer_model.encode([text2], convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(embedding1, embedding2)
    return similarity.item()

def preprocess_resume(uploaded_file):
    # Get the file extension
    file_extension = uploaded_file.name.split('.')[-1]
    
    # Extract text based on the file extension
    if file_extension == 'txt':
        # For plain text files (TXT)
        resume_text = uploaded_file.read().decode('utf-8')
    elif file_extension == 'pdf':
        # For PDF files
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        resume_text = ''
        for page_num in range(len(pdf_reader.pages)):
            resume_text += pdf_reader.pages[page_num].extract_text()
    elif file_extension == 'docx':
        # For DOCX files
        doc = docx.Document(uploaded_file)
        resume_text = ''
        for paragraph in doc.paragraphs:
            resume_text += paragraph.text + '\n'
    else:
        st.error("Unsupported file format. Please upload a TXT, PDF, or DOCX file.")
        return None
    
    return resume_text
# Define a list of common skills
common_skills = ["Java", "Python", "C++", "HTML", "CSS", "AWS", "SalesForce", "Android Studio", "NLP", "DeepFace", "React Native", "Machine learning"]

# Function to extract skills from resume text
def extract_skills(resume_text):
    extracted_skills = []
    for skill in common_skills:
        if skill.lower() in resume_text.lower():
            extracted_skills.append(skill)
    return extracted_skills


def main():
    st.title("Resume Scoring and Email Sending Portal")
    
    # Add a button to choose the scoring model (optional)
    selected_model = st.selectbox("Choose a scoring model", ["paraphrase-MiniLM-L6-v2", "all-mpnet-base-v2"])
    
    # Add an input box for the candidate's name
    candidate_name = st.text_input("Candidate's Name")
    
    # Add an input box for the candidate's email
    candidate_email = st.text_input("Candidate's Email")
    
    uploaded_file = st.file_uploader("Upload a resume", type=["txt", "pdf", "docx"])
    if uploaded_file is not None and candidate_name:
        # Process the uploaded resume
        resume_text = preprocess_resume(uploaded_file)
        
        # Extract skills from the resume
        # Call the function to extract skills
        candidate_skills = extract_skills(preprocess_resume(uploaded_file))

        
        # Calculate similarity score
        job_description = "Iedicated and hardworking student who is committed to achieving excellence in every task I undertake. I believe in putting in the extra effort required to meet and exceed expectations. I am open to suggestions and actively incorporate feedback into my work, allowing me to continually refine my abilities and deliver better results. I'd like to say that I have a strong interest in my field of study and a real desire to keep learning. This internal drive pushes me to keep up with the latest industry trends and developments, which lets me bring new ideas and a different point of view to the team. Also, I am polite in my ways and I value other people's emotions while giving space for myself.Git, Postman API , Android Studio, MATLAB, TinkerCad. I believe that these qualities, coupled with my passion for learning, make me an ideal candidate for the job,NLP,deepface python"
        similarity_score = calculate_similarity(resume_text, job_description, selected_model)
        
        # Set the threshold (you can adjust this as needed)
        threshold = 0.3
        if similarity_score >= threshold:
            st.success("Congratulations! Your resume is aligned with the job requirements.")
            
            # If the candidate's email is not provided, try to extract it from the resume
            if not candidate_email:
                candidate_email = extract_email_from_text(resume_text)
            
            # Generate the personalized email content
            if candidate_skills:
                email_content = generate_email_with_bloom(candidate_name, candidate_skills)
                print(email_content)
                # Introduce a delay between API requests
                time.sleep(100)  # Delay for 100 seconds before making the API request

                # Use the Mailgun API to send the email
                mailgun_api_key =os.getenv("mailgun_api_key")
                mailgun_domain = os.getenv("mailgun_domain")
                from_email = os.getenv("MAIL")
                to_email = candidate_email
                subject = "Interview Invitation"

                email_sent = send_email(mailgun_api_key, mailgun_domain, from_email, to_email, subject, email_content)
                if email_sent:
                    st.info("An email has been sent to the candidate.")
                else:
                    st.warning("Email sending failed.")

        else:
            st.warning("Your resume does not meet the alignment threshold.")

if __name__ == "__main__":
    main()
