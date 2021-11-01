import time
import json
import smtplib, ssl
from pushsafer import Client
from os.path import exists
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Get titles and links
def get_data(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(3)
    elements1 = driver.find_elements(By.CLASS_NAME, '_mm360j')
    elements2 = driver.find_elements(By.CLASS_NAME, '_1whrsux9')
    titles = []
    links = []
    for e1, e2 in zip(elements1, elements2):
        titles.append(e2.text)
        links.append(e1.get_attribute('href'))
    data = dict(zip(titles, links))
    return data

# Check if there are any new titles
def difference(new_titles, old_titles):
    diff = [i for i in new_titles if i not in old_titles]
    return diff

# Send email
def send_email(title, url):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = "your sender gmail"
    receiver_email = "email of whom you want to send it to"
    password = "password for sender_email"
    subject = title
    body = url
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    print('email has been sent')

# Save titles to a json file
def store_titles(titles):
    with open('titles.json', 'w') as f:
        json.dump(titles, f)
    print("titles saved to json")

# Function to run the above in proper order
def runit(url):
    data = get_data(url)
    new_titles = list(data.keys())
    new_urls = list(data.values())
    with open('titles.json', 'r') as f:
        old_titles = json.load(f)
    diff_titles = difference(new_titles, old_titles)
    if diff_titles:
        for title in diff_titles:
            send_email(title, data[title])
    store_titles(new_titles)

url = "your url here"
    runit(url)
else:
    titles = list(get_data(url).keys())
    store_titles(titles)
