import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

#getting weather report
def get_weather(city, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description']
        wind_speed = data['wind']['speed']
        city_name = data['name']
        country = data['sys']['country']

        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%I:%M %p')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%I:%M %p')

        weather_report = f"Weather Report for {city_name}, {country}:\n"
        weather_report += f"Temperature: {round(temperature)} F (Feels like: {round(feels_like)} F)\n"
        weather_report += f"Condition: {weather_description.capitalize()}\n"
        weather_report += f"Humidity: {humidity}%\n"
        weather_report += f"Wind Speed: {round(wind_speed)} mph\n"
        weather_report += f"Sunrise: {sunrise}\n"
        weather_report += f"Sunset: {sunset}\n"

        return weather_report
    else:
        return "Error: Unable to fetch weather data."

api_key = '' #your api key
city = '' #city you want to use
weather_report = get_weather(city, api_key)
print(weather_report) #dont need, use to test if the code is working

#sending text message via email
sender_email = "" #your email
sender_password = "" #your password

phone_number = "" #receiving phone number
carrier_gateway = "" #receiving number carrier gateway
recipient_email = f"{phone_number}@{carrier_gateway}"

message = weather_report

def send_email(message, recipient_email, sender_email, sender_password):
    msg = MIMEText(message)
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Weather Report"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Text message sent successfully!")
    except Exception as e:
        print(f"Failed to send message: {e}")

#scheduling text message
def job():
    city = '' #city you want to use
    api_key = '' #your api key
    weather_report = get_weather(city, api_key)

    phone_number = "" #receiving phone number
    carrier_gateway = "" #receiving number carrier gateway
    recipient_email = f"{phone_number}@{carrier_gateway}"

    sender_email = "" #your email
    sender_password = "" #your password

    send_email(weather_report, recipient_email, sender_email, sender_password)

schedule.every().day.at("8:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
