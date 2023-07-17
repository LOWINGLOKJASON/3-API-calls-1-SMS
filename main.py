# ****************************************************************
# Name: Wing Lok LO
# Link: https://replit.com/join/gdrsrbvbfk-lowinglokjason
# ****************************************************************

# Import packages
from flask import Flask, render_template
import os
import requests
from twilio.rest import Client
from datetime import datetime

# Define log message
def log_message(messages):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  log_entry = f"{timestamp}: {messages}\n"
  
  # Write to the text file
  with open('messages.txt', 'a') as file:
    file.write(log_entry)

app = Flask('app')

# Define the main page
@app.route('/')
def hello_world():
  return render_template("index.html")

# Define the success page
@app.route('/sms')
def send_sms():
  
  # Connect to Harry Potter API
  harry_potter_url = 'https://hp-api.onrender.com/api/characters'
  response = requests.get(harry_potter_url)
  characters = response.json()[0]['name'] # Print only Harry Potter
  
  # Connect to OpenWeather API
  openweather_api_key = 'fe8864f0805d25db6c7d08959d89dd60'
  city = 'Toronto' 
  weather_api_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={openweather_api_key}'
  response = requests.get(weather_api_url)
  weather_data = response.json() # Print weather
  
  # Connect to OpenNotify API
  iss_api_url = 'http://api.open-notify.org/iss-now.json'
  response = requests.get(iss_api_url)
  iss_data = response.json() # Print ISS coordinates
  
  # Send data through Twilio API
  account_sid = os.environ['TWILIO_ACCOUNT_SID']
  auth_token = os.environ['TWILIO_AUTH_TOKEN']
  
  client = Client(account_sid, auth_token)
  
  # Message content
  message = client.messages \
  .create(
    body=f"Harry Potter API Characters: {characters}\n" \
    f"Weather in {city}: {weather_data['weather'][0]['description']}\n" \
    f"Current ISS coordinates: {iss_data['iss_position']}",
    from_='+19897955674', # Sender Phone Number
    to='+17059885764'  # Receiver Phone Number
  )
  # Print message SID
  print(message.sid)

  # Log the sent message
  log_message(message)
  
  return render_template("success.html")

app.run(host='0.0.0.0', port=8080)
