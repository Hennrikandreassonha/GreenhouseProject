import lib.umail
from secrets import secrets

# Email details
sender_email = secrets['sender-email']
sender_app_password = secrets['sendEmail-password']
email_subject = '    🌞Uppdatering från växthus🌞'

# Define the email content with a green background'


def email_content(temp, humidity, soilmoisture, light):
    return f"""
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
            margin-top: 150px;
            border-radius: 25px;
            position: absolute;
            top: 150px;
            left: 50%;
            transform: translate(-50%, -50%);
            text-align: center;
            font-size: 24px;
            padding: 2rem 1rem;
            min-height: 3em;
            width: 60%;
            resize: both;
            border: 5px solid #b0e2ff;
        }}
    </style>
</head>
<body>
    <div id="pic">
        <div id="card">
            <p>Det är <strong>{temp}°</strong></p>
            <p>Fuktigheten i luften är <strong>{humidity}</strong></p>
            <p>Fuktigheten i jorden är <strong>{soilmoisture}%</strong></p>
            <p>Det är <strong>{light}</strong> ljust</p>
        </div>
    </div>
</body>
</html>
"""


def send_email(reciever, temp, humidity, soilmoisture, light):

    smtp = lib.umail.SMTP('smtp.gmail.com', 465, ssl=True)
    smtp.login(sender_email, sender_app_password)
    smtp.to(reciever)
    smtp.write(f"Subject: {email_subject}\n")
    smtp.write("Content-Type: text/html\n")
    smtp.write("\n")  # Empty line to separate headers from content
    smtp.write(email_content(temp, humidity, soilmoisture, light))
    smtp.send()
    smtp.quit()


send_email("henrik1995a@live.se", 123, 123, 123, 123)