# RRR Portal

<!-- ![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg) -->

## Table of Contents

- [Description](#description)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
<!-- - [Contributing](#contributing)
- [License](#license) -->

## Description

This project is a Streamlit-based web application that scores resumes based on their alignment with a job description and sends personalized interview invitations via email. It utilizes Sentence Transformer models and other libraries to achieve this functionality.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6+
- Pip (Python package manager)
- A Mailgun account with an API key and domain (for sending emails)
- Hugging Face API access (for the Sentence Transformer model)
- Git (optional, for version control)

## Installation

1. Clone the repository to your local machine (if you haven't already):

   ```bash
   git clone https://github.com/Girishtheja/Resume-Ranking-Report.git
2. Navigate to the project directory:
 
   ```bash
    cd Resume-Ranking-Report
3. Create a virtual environment (recommended):
   ```bash
    python3 -m venv venv
4. Activate the virtual environment:

   - On Windows:
       ```bash
       venv\Scripts\activate
    
   - On macOS and Linux:
       ```bash
       source venv/bin/activate

5. Install the project dependencies from the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt


## Configuration
1. Create a .env file in the project directory to store your environment variables. These variables include API keys and other sensitive information.

- look into the .env.example file for format:
   ```bash
    API_URL=https://api-inference.huggingface.co/models/bigscience/bloom
    headers=Bearer your-huggingface-api-key
    mailgun_api_key=your-mailgun-api-key
    mailgun_domain=your-mailgun-domain
    MAIL=your-email@example.com

Replace the placeholders (`your-huggingface-api-key`, `your-mailgun-api-key`, `your-mailgun-domain`, and `your-email@example.com`) with your actual values.

2. Save the `.env` file.

## Usage

1. Run the Streamlit app:

    ```bash
    streamlit run streamlit_app.py

2. Access the app in your web browser by opening the URL provided by Streamlit.
3. Upload a resume, enter the candidate's name and email, and click the "Score Resume" button.
4. The app will score the resume based on its alignment with a job description and send a personalized email to the candidate if the score meets the threshold.


