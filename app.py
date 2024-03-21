from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os 
import google.generativeai as genai
import PyPDF2 as pdf

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



def get_gemini_response(jd,text):
    input_prompt=f"""
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst,Machine learning
and big data engineer choose any one according to the jd(job description) provided below .Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving the resume. 
Assign the percentage Matching based on Jd and the missing keywords with high accuracy.
resume:
{text}
description:
{jd}

I want the response in one single string having the structure like this
{{"JD Match":"%",
"MissingKeywords:[]",
"Profile Summary":""}}
"""
    print(input_prompt)
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input_prompt)
    return response.text


def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text


# streamlit app
st.title("Smart ATS")
st.text("Improve Your ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type='pdf',help="Please upload the file")
submit=st.button("Submit")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_response(jd,text)
        st.subheader(response)


