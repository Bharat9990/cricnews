import requests
from bs4 import BeautifulSoup
from email.message import EmailMessage
import smtplib
import ssl
import gradio as gr
import creds 

def send_email(email_address, subject, content):
    email_sender = creds.email
    email_password = creds.password
    email_receiver = email_address

    subject = subject
    body = content
    try:
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_receiver
        em['Subject'] = subject
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_receiver, em.as_string())

    except Exception as e:
        print(f"Error sending email reminder to {email_address}: {e}")

def send_news(user_name, email):
    s=""
    c=0
    r=requests.get('https://www.cricbuzz.com/cricket-news/latest-news')
    url_content=r.content
    soup=BeautifulSoup(url_content,'html.parser')
    title=soup.title
    title.string
    articles = soup.find_all('div', class_='cb-col cb-col-100 cb-lst-itm cb-pos-rel cb-lst-itm-lg')
    for article in articles:
        link=article.find('a',attrs={'class':"cb-nws-hdln-ancr text-hvr-underline"})
        l=link.get('href')
        title_art=link.get('title')
        info_art=article.find('div', class_='cb-nws-intr')
        c=c+1;
        s=s+str(c)+". "
        s=s+title_art+"\n"
        s=s+info_art.string+"\n"+"https://www.cricbuzz.com/"+l+"\n"
    subject="Daily Cricket Dose for "+user_name
    email=str(email)
    send_email(email,subject,s)
    return s

# Define the Gradio interface
input_components = [
    gr.components.Textbox(label="Enter Your Name"),
    gr.components.Textbox(label="Email"),
]

output_component = gr.components.Textbox()

iface = gr.Interface(
    fn=send_news,
    inputs=input_components,
    outputs=output_component,
    title="Cricket News Sender",
    description="Provide Information to recive cricket news on your E-mail",
)

if __name__ == "__main__":
    iface.launch()