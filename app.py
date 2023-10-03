import streamlit as st
import gensim
import requests

# Load a pre-trained Word2Vec model (you need to provide the path to the model file)
word2vec_model = gensim.models.Word2Vec.load("path_to_word2vec_model")

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
    print(resume_text)
    return resume_text

def calculate_similarity(text1, text2):
    # Use the word embedding model to calculate the cosine similarity between two texts
    vector1 = sum(word2vec_model[word] for word in text1.split()) / len(text1.split())
    vector2 = sum(word2vec_model[word] for word in text2.split()) / len(text2.split())
    similarity = vector1.dot(vector2) / (vector1.norm() * vector2.norm())
    return similarity

def generate_email(candidate_name, candidate_skills):
    # Use GPT-3 to generate a personalized email
    prompt = f"Dear {candidate_name},\n\nWe are pleased to inform you that your skills in {candidate_skills} align well with the job requirements. We would like to invite you to the next round of interviews."
    # Use your GPT-3 integration here to generate the email content
    # Placeholder response for demonstration
    response = "Congratulations! Your resume is aligned with the job requirements. We would like to invite you to the next round of interviews."
    return response

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

def main():
    st.title("Resume Scoring and Email Sending Portal")
    
    # Add a button to choose the scoring model (optional)
    selected_model = st.selectbox("Choose a scoring model", ["paraphrase-MiniLM-L6-v2", "all-mpnet-base-v2"])

    uploaded_file = st.file_uploader("Upload a resume", type=["txt", "pdf", "docx"])
    if uploaded_file is not None:
        # Process the uploaded resume
        resume_text = preprocess_resume(uploaded_file)
        
        # Calculate similarity score
        job_description = "Our ideal candidate has experience in software development."
        similarity_score = calculate_similarity(resume_text, job_description)
        
        # Set the threshold (you can adjust this as needed)
        threshold = 0.7
        if similarity_score >= threshold:
            st.success("Congratulations! Your resume is aligned with the job requirements.")
            
            # Generate the personalized email content
            candidate_name = "John Doe"  # Placeholder candidate name
            candidate_skills = "software development"  # Placeholder candidate skills
            email_content = generate_email(candidate_name, candidate_skills)

            # Use the Mailgun API to send the email
            api_key = "YOUR_MAILGUN_API_KEY"
            domain = "YOUR_MAILGUN_DOMAIN"  # Example: "sandbox123.mailgun.org"
            from_email = "sender@example.com"
            to_email = "candidate@example.com"
            subject = "Interview Invitation"

            email_sent = send_email(api_key, domain, from_email, to_email, subject, email_content)
            if email_sent:
                st.info("An email has been sent to the candidate.")
            else:
                st.warning("Email sending failed.")

        else:
            st.warning("Your resume does not meet the alignment threshold.")

if __name__ == "__main__":
    main()
