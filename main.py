from personal_data import api_id,  my_email, my_password
import smtplib
import requests

parameters = {
    "lat": 37.034409,
    "lon": 27.430540,
    "exclude": "current,minutely,daily",
    "appid": api_id}

# request data by passing the end point URL and the parameters
# that contain lat and long of the location and the API key
data = requests.get(url="https://api.openweathermap.org/data/2.5/onecall", params=parameters)
# if there is an error code, an exception will be raised
data.raise_for_status()

# transform the request into the json format
weather_data = data.json()

# check if it going to rain in the next 12 hours
# create a list of forecast dictionaries for next 12 hours
list_of_dictionaries = weather_data["hourly"][:12]
# go through each of them to see if weather id is below 700
# (anything below 700 is for rain https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2)
will_rain = False
for hour_dict in list_of_dictionaries:
    condition_code = hour_dict["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

# if there is going to be rain in the next 12 hours, send an alert email
if will_rain:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=my_password)
        connection.sendmail(from_addr=my_email,
                            to_addrs=my_email,
                            msg="Subject: Weather alert!\n\nIt's going to rain today. Bring an umbrella!")