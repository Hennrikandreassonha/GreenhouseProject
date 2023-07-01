#This is a file that is used to quickly test the mail function without having a having to run the main loop.

eveningValues = {
    "temp": 22,
    "humidity": 54,
    "groundmoist": 900,
    "light": 11
}

nightValues = {
    "temp": 15,
    "humidity": 20,
    "groundmoist": 600,
    "light": 4
}

dayValues = {
    "temp": 27,
    "humidity": 54,
    "groundmoist": 1300,
    "light": 16
}
def email_content(dayvalues, nightvalues, eveningvalues):
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
            padding: 2rem;
            margin-top: 900px;
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
            <p>Temp: <strong>{dayvalues["temp"]}°</strong></p>
            <p>Fuktigheten i luft: <strong>{dayvalues["humidity"]}</strong></p>
            <p>Fuktigheten i jord: <strong>{dayvalues["groundmoist"]}%</strong></p>
            <p>Ljusstryka: <strong>{dayvalues["light"]}</strong> ljust</p>

            <br>
            <p>Klockan <strong>18</strong></p>
            <p>Temp: <strong>{eveningvalues["temp"]}°</strong></p>
            <p>Fuktigheten i luft: <strong>{eveningvalues["humidity"]}</strong></p>
            <p>Fuktigheten i jord: <strong>{eveningvalues["groundmoist"]}%</strong></p>
            <p>Ljusstryka: <strong>{eveningvalues["light"]}</strong> ljust</p>
            
            <br>
            <p>Klockan <strong>03</strong></p>
            <p>Temp: <strong>{nightvalues["temp"]}°</strong></p>
            <p>Fuktigheten i luft: <strong>{nightvalues["humidity"]}</strong></p>
            <p>Fuktigheten i jord: <strong>{nightvalues["groundmoist"]}%</strong></p>
            <p>Ljusstryka: <strong>{nightvalues["light"]}</strong> ljust</p>
        </div>
    </div>
</body>
</html>
"""
from mysecrets import secrets
import lib.umail

sender_email = secrets['sender-email']
sender_app_password = secrets['sendEmail-password']
email_subject = '🌞Uppdatering från växthus🌞'

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

try:
    send_email("henrik1995a@live.se", dayValues, nightValues, eveningValues)
    print("Success! Mail has been sent")
    #Email has been sent.
except Exception as e:
        print(f'Failed to send email: {e}')