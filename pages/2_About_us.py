from openai import OpenAI
import streamlit as st
import os

openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

# Titles
st.set_page_config(page_title="About us")
st.header('About us')
st.write("""
         Welcome to our About Us page! We are a team of students, a team dedicated to utilize AI to support student applications. 
         Here, you'll find information about our goals, achievements, and team members.
         """)
# Our Mission
st.header('Our Mission')
st.write("""
         Our mission is to harness the transformative power of AI to revolutionize the student application process. 
         We aim to provide innovative tools and platforms that simplify and enhance the experience for students worldwide, 
         enabling them to unlock their full potential and achieve their academic and career aspirations.
         """)
# Our Team
st.header('Our Team')
# Using columns for team members
col1, col2, col3 = st.columns(3)

with col1:
    st.image(os.path.join('Photos', 'About us', 'People', 'People_1.webp'), caption='Team Member 1')
    st.write('Role: Position')
with col2:
    st.image(os.path.join('Photos', 'About us', 'People', 'People_2.webp'), caption='Team Member 2')
    st.write('Role: Position')
with col3:
    st.image(os.path.join('Photos', 'About us', 'People', 'People_3.webp'), caption='Team Member 3')
    st.write('Role: Position')


# Contact Us
st.header('Contact Us')
st.write('Email: tshan.work@gmail.com')

# Add an image
st.image('Photos\About us\About_us_photo.webp', caption='Caption for your image.')

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# # Email settings (example with Gmail)
# smtp_server = 'smtp.gmail.com'
# smtp_port = 587
# username = os.environ.get("gmail_username")
# password = os.environ.get("gmail_password")

# def send_email(name, sender_email, message):
#     # Create the email headers and content
#     msg = MIMEMultipart()
#     msg['From'] = username
#     msg['To'] = username  # Sending the email to yourself
#     msg['Subject'] = 'New Contact Form Submission'
#     body = f'Name: {name}\nEmail: {sender_email}\nMessage: {message}'
#     msg.attach(MIMEText(body, 'plain'))
    
#     # Send the email
#     server = smtplib.SMTP(smtp_server, smtp_port)
#     server.starttls()
#     server.login(username, password)
#     text = msg.as_string()
#     server.sendmail(username, username, text)
#     server.quit()

# # Streamlit form for contact information
# st.header('Get in Touch')
# with st.form(key='contact_form'):
#     name = st.text_input('Name')
#     email = st.text_input('Email')
#     message = st.text_area('Message')
#     submit_button = st.form_submit_button('Submit')
#     if submit_button:
#         send_email(name, email, message)  # Call the send_email function on form submission
#         st.write('Thank you, we have received your message.')


# st.markdown("# General AI Chatbot")
# st.sidebar.header("General AI Chatbot")
# st.write("This demo helps you figure out general questions. Enjoy!")

