from personal_data import api_id, \
    twilio_account_sid, twilio_auth_token, my_number, twilio_number
import requests
from twilio.rest import Client

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

# if there is going to be rain in the next 12 hours, send an SMS alert using Twilio
if will_rain:
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
                                  body="Weather alert! It's going to rain today. Bring an umbrella!",
                                  from_=twilio_number,
                                  to=my_number
                                )
    print(message.status)