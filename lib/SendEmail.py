import lib.umail
from mysecrets import secrets

# Email details
sender_email = secrets['sender-email']
sender_app_password = secrets['sendEmail-password']
email_subject = '🌞Uppdatering från växthus🌞'

# Define the email content with a green background'


def email_content(dayvalues, nightvalues, eveningvalues):
    daytemp = dayvalues["temp"]
    dayhumid = dayvalues["humidity"]
    daygroundmoist = dayvalues["groundmoist"]
    daylight = dayvalues["light"]

    eveningtemp = eveningvalues["temp"]
    eveninghumid = eveningvalues["humidity"]
    eveninggroundmoist = eveningvalues["groundmoist"]
    eveninglight = eveningvalues["light"]

    nighttemp = nightvalues["temp"]
    nighthumid = nightvalues["humidity"]
    nightgroundmoist = nightvalues["groundmoist"]
    nightlight = nightvalues["light"]

    return f"""
<html>
<head>
    <style>
        #pic {{
            background-image: url("https://cdn.wallpapersafari.com/63/50/1adgR2.jpg");
            background-repeat: no-repeat;
            background-size: cover;
            height: 1500px;
            width: 500px;
        }}

        #card {{
            background-color: white;
            margin-top: 850px;
            border-radius: 25px;
            position: absolute;
            left: 50%;
            transform: translate(-50%, -70%);
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
        <div id="card" style="background-color: white;">

            <p>Klockan <strong>12</strong></p>
            <p>Temp: <strong>{daytemp}°</strong></p>
            <p>Fuktighet luft: <strong>{dayhumid}</strong></p>
            <p>Fuktighet jord: <strong>{daygroundmoist}</strong></p>
            <p>Ljusstyrka: <strong>{daylight}</strong></p>

            <br>
            <p>Klockan <strong>18</strong></p>
            <p>Temp: <strong>{eveningtemp}°</strong></p>
            <p>Fuktighet luft: <strong>{eveninghumid}</strong></p>
            <p>Fuktighet jord: <strong>{eveninggroundmoist}</strong></p>
            <p>Ljusstyrka: <strong>{eveninglight}</strong></p>
            
            <br>
            <p>Klockan <strong>03</strong></p>
            <p>Temp: <strong>{nighttemp}°</strong></p>
            <p>Fuktighet luft: <strong>{nighthumid}</strong></p>
            <p>Fuktighet jord: <strong>{nightgroundmoist}%</strong></p>
            <p>Ljusstyrka: <strong>{nightlight}</strong></p>
        </div>
    </div>
</body>
</html>
"""


def send_email(reciever, dayvalues, nightvalues, eveningvalues):

    smtp = lib.umail.SMTP('smtp.gmail.com', 465, ssl=True)
    smtp.login(sender_email, sender_app_password)
    smtp.to(reciever)
    smtp.write(f"Subject: {email_subject}\n")
    smtp.write("Content-Type: text/html\n")
    smtp.write("\n")  # Empty line to separate headers from content
    smtp.write(email_content(dayvalues, nightvalues, eveningvalues))
    smtp.send()
    smtp.quit()
