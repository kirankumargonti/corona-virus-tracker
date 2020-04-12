from bs4 import BeautifulSoup
import smtplib
import time
from datetime import date
import requests
from email.message import EmailMessage

EMAIL_ADDRESS = "example@gmail.com"  # sender gmail address
EMAIL_PASSWORD = "**************"  # sender gmail password


def corona_updates():
    # for global information use the below url
    # url = "https://www.worldometers.info/coronavirus/"
    indiaURL = "https://www.worldometers.info/coronavirus/country/india/"  # for india
    r = requests.get(indiaURL)
    s = BeautifulSoup(r.text, "html.parser")
    data = s.find_all("div", class_="maincounter-number")
    total_cases = data[0].text.strip()
    total_recoveries = data[2].text.strip()
    total_deaths = data[1].text.strip()

    # Mail Function
    sendMail(total_cases, total_recoveries, total_deaths)


def sendMail(total_cases, total_recoveries, total_deaths):
    # add more emial addresses to send the updates
    contacts = ['jhondoe@gmail.com',
                "exmaple1@gmail.com", "exmaple2@gmail.com"]
    email = EmailMessage()
    email['Subject'] = "Corona Virus (COVID-19) Today's Update"
    email['From'] = EMAIL_ADDRESS
    # email['To'] = EMAIL_ADDRESS # To send a Single Person
    email['To'] = ', '.join(contacts)  # for multiple persons
    email.add_alternative("""\
    <!DOCTYPE html>
    <html lang="en">
    <body style="background-color: aliceblue;
    padding: 50px;
    font-family: 'Trebuchet MS', 'Lucida Sans Unicode', 'Lucida Grande', 'Lucida Sans', Arial, sans-serif">
        <div style="padding: 20px;
        border-radius: 10px;
        background-color:#ffffff">
            <h1>Corona-virus Cases in <span style="color: teal">India</span> - """+str(date.today().strftime("%d/%m/%Y"))+"""</h1>
                <h2 style="color: orange;">Total Cases: """+total_cases + """</h2>
                <h2 style="color: green;">Total Recoveries: """+total_recoveries + """</h2>
                <h2 style="color: red;">Total Deaths: """+total_deaths + """</h2>
            <h1>Stay Home <span style="color: teal">Stay Safe.!</span></h1>
            <p>Made with <span style="color: red"> &#10084;</span> by <a target="_blank"
                    href="https://github.com/kirankumargonti">Kirankumar Gonti</a></p>
        </div>
    </body>
    </html>""", subtype="html")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(email)
        print("Hey Email has been sent.!")


while(True):
    corona_updates()
    time.sleep((60*60)*24)  # Runs after every 24 hours
