import time
import requests
from datetime import datetime
from email.mime.text import MIMEText
import smtplib

MY_LAT = 35.68576349032452 # Your latitude
MY_LONG = 139.7527943992632 # Your longitude

my_email = "test@tmail.com"
password = "QWERTY"

while True:
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    print(f"iss_lat: {iss_latitude} / my_lat: {MY_LAT}")
    print(f"iss_long: {iss_longitude} / my_long: {MY_LONG}")

    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT + 5 > iss_latitude > MY_LAT - 5 and MY_LONG + 5 > iss_longitude > MY_LONG - 5:

        parameters = {
            "lat": MY_LAT,
            "lng": MY_LONG,
            "formatted": 0,
        }

        response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
        response.raise_for_status()
        data = response.json()
        sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
        sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
        print(sunrise)
        print(sunset)

        time_now = datetime.now()
        print(time_now.hour)

        #If the ISS is close to my current position
        # and it is currently dark
        # Then send me an email to tell me to look up.
        # BONUS: run the code every 60 seconds.
        if time_now.hour < sunrise or time_now.hour > sunset:
            # MIMETextオブジェクトを作成し、メールの内容を設定する
            msg = MIMEText("Look up!", 'plain', 'utf-8')
            msg['Subject'] = "The ISS is close to you!"
            msg['From'] = my_email
            msg['To'] = my_email

            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=my_email, password=password)
                connection.send_message(msg)

    time.sleep(10)