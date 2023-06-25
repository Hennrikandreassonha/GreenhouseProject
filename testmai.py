from lib.SendEmail import send_email


eveningValues = {
    "temp": 123,
    "humidity": 123,
    "groundmoist": 123,
    "light": 123
}

nightValues = {
    "temp": 456,
    "humidity": 456,
    "groundmoist": 456,
    "light": 456
}

dayValues = {
    "temp": 789,
    "humidity": 789,
    "groundmoist": 789,
    "light": 789
}

send_email("henrik1995a@live.se", dayValues, nightValues, eveningValues)