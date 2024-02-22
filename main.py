import requests
from datetime import datetime
import smtplib

MY_LAT = 50.6903  # Your latitude
MY_LONG = -179.4317  # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


# Your position is within +5 or -5 degrees of the ISS position.

def isItClose():
    if abs(MY_LAT - iss_latitude) <= 5 and abs(MY_LONG - iss_longitude) <= 5:
        return True
    else:
        return False


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
current_hour = datetime.now().hour


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

# Function to tell me if it's daytime or nighttime

def dayTime():
    if 6 <= current_hour <= 17:
        return "Daytime"
    else:
        return "Night Time"


# Email credentials portion of program.
test_email = ""
my_email = ""
my_password = ""


# Email sending and program function
day_mess = "It's daytime, might be hard to see but go out, it's above you"
night_mess = "It's night time, you can see the iss above you! Good luck!"

if isItClose():
    if dayTime() == "Daytime":
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=test_email,
                                msg=f"Subject: ISS UP ABOVE!\n\n {day_mess}")
        print("Sent email")
    elif dayTime() == "Night Time":
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=test_email,
                                msg=f"Subject: ISS UP ABOVE!\n\n {night_mess}")
        print("Sent email")
else:
    print("It's not time yet")
