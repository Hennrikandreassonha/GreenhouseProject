import smtplib
from email.message import EmailMessage
from secrets import secrets

# This file contains code that is used for sending email
# I did not want to put all the ugly hmtl code in main.py

senderEmail = "karinsvaxthus@gmail.com"

emailPassword = 'xjlxvhcqqxyhpsvs'
recieverEmail = 'henrik1995a@live.se'


def send_email(recieverEmail, temp, humid, earthHumid, light):
    msg = EmailMessage()
    msg.add_alternative(html_content(temp, humid, earthHumid, light), subtype='html')

    msg['Subject'] = 'Uppdatering från växthuset'
    msg['From'] = secrets['sender-email']
    msg['To'] = recieverEmail

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(secrets['sender-email'], secrets['sendEmail-password'])
    server.send_message(msg)
    server.quit()

def html_content(temp, humid, earthHumid, light):
    
    return f'''
    <html>

    <head>
        <style>
            #pic {{
                background-image: url("https://cdn.wallpapersafari.com/63/50/1adgR2.jpg");
                background-repeat: no-repeat;
                background-size: 100%;
                height: 1000px;
                width: 500px;
            }}

            #card {{
                background-color: white;
                padding: 2rem;
                margin-top: 200px;
                border-radius: 25px;
                margin-top: 300px;
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                font-size: 24px;
                border: 10px solid black;
                padding: 2rem 1rem;
                min-height: 3em;
                width: 60%;
                resize: both;
                background: linear-gradient(to top, rgba(#cffffe, 0.3), rgba(#f9f7d9, 0.3), rgba(#fce2ce, 0.3), rgba(#ffc1f3, 0.3));
                border-image: url("data:image/svg+xml;charset=utf-8,%3Csvg width='100' height='100' viewBox='0 0 100 100' fill='none' xmlns='http://www.w3.org/2000/svg'%3E %3ClinearGradient id='g' x1='0%25' y1='0%25' x2='0%25' y2='100%25'%3E%3Cstop offset='0%25' stop-color='%23cffffe' /%3E%3Cstop offset='25%25' stop-color='%23f9f7d9' /%3E%3Cstop offset='50%25' stop-color='%23fce2ce' /%3E%3Cstop offset='100%25' stop-color='%23ffc1f3' /%3E%3C/linearGradient%3E %3Cpath d='M1.5 1.5 l97 0l0 97l-97 0 l0 -97' stroke-linecap='square' stroke='url(%23g)' stroke-width='3'/%3E %3C/svg%3E") 1;
            }}
        </style>
    </head>

    <body>

        <div id="pic">
            <div id="card">

                <p>Det är <strong>{temp}°</strong></p>
                <p>Fuktigheten i luften är <strong>{humid}</strong></p>
                <p>Fuktigheten i jorden är: <strong>{earthHumid}%</strong></p>
                <p>Det är <strong>{light}</strong> ljust</p>

            </div>
        </div>
    </body>

    </html>
        '''

send_email('henrik1995a@live.se', '123', '123', '123','123',)