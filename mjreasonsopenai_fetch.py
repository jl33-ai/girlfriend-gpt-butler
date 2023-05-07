from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os
import random
import requests
import json
import openai
from datetime import datetime
from datetime import date

# If modifying these scopes, delete the file token.json.

SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = '1Z6UyMYIcWx81b9Lb9qvKwN4yXGvK3ff5o2TyAHn1jY4'

#openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = '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'

# Get today's date and days counter
today = datetime.now().strftime('%Y-%m-%d')
doc_date = datetime.now().strftime('%d/%m')
a = datetime(2022,3,30)
b = datetime.now()
days_since = (b-a).days

# Get the random sentence
SENTENCES_URL = "https://pastes.io/raw/hfeij7iupp"
response = requests.get(SENTENCES_URL)
sentences = response.text.splitlines()
random_sentence = random.choice(sentences)

# Get weather
def get_weather(latitude, longitude):
    url = "https://api.open-meteo.com/v1/forecast?latitude=-37.93&longitude=145.00&daily=weathercode,temperature_2m_max,temperature_2m_min,uv_index_max&forecast_days=1&timezone=auto"
    response = requests.get(url)
    return response.json()

def weather_to_emoji(weather_code):
    weather_emojis = {
        0: "☀️",
        1: "🌤️",
        2: "⛅",
        3: "🌥️",
        45: "🌫️",
        48: "🌫️",
        51: "🌦️",
        53: "🌦️",
        55: "🌦️",
        56: "🌧️",
        57: "🌧️",
        61: "🌧️",
        63: "🌧️",
        65: "🌧️",
        66: "🌧️",
        67: "🌧️",
        71: "❄️",
        73: "❄️",
        75: "❄️",
        77: "❄️",
        80: "🌦️",
        81: "🌦️",
        82: "🌦️",
        85: "🌨️",
        86: "🌨️",
        95: "⛈️",
        96: "⛈️",
        99: "⛈️",
    }
    return weather_emojis.get(weather_code, "❓")
        


    

# Get random cat fact

def get_cat_fact():
    response = requests.get("https://cat-fact.herokuapp.com/facts/random")
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return "Failed to retrieve cat fact"

'''
# Get the UV index using OpenUV API
API_KEY = 'openuv-96wrs0rlgxlbvdz-io'  # Replace with your API key
latitude = -37.783660
longitude = 145.034960

url = f'https://api.openuv.io/api/v1/uv?lat={latitude}&lng={longitude}'
headers = {
    'x-access-token': API_KEY,
}


response = requests.get(url, headers=headers)

if response.status_code == 200:
    uv_data = response.json()
    uv_index = round(uv_data['result']['uv_max'], 1)
else:
    uv_index = "Could not be fetched"

'''

# Accessing the mj calendar

def read_structural_elements(elements, doc_date):
    tasks = []
    found_date = False
    for value in elements:
        if 'table' in value:
            table = value.get('table')
            for row in table.get('tableRows'):
                if not found_date: 
                    day_index = 0
                cells = row.get('tableCells')
                if not found_date:
                    for cell in cells:
                        # Find date
                        for value in cell.get('content'):
                            for element in (value.get('paragraph').get('elements')):
                                text_run = element.get('textRun')
                                if text_run:
                                    cell_text = text_run.get('content').strip()
                                    if cell_text == doc_date:
                                        found_date = True
                                        # print("Found Date:", cell_text, "at index", day_index)
                                        break
                        if not found_date: 
                            day_index += 1
                else:
                    cell = cells[day_index]
                    for value in cell.get('content'):
                        for element in (value.get('paragraph').get('elements')):
                            text_run = element.get('textRun')
                            if text_run:
                                tasks.append(text_run.get('content').strip())

                    # Make  dictionairy that has the current day and then next week of things, indexed by Day and Date. 
                    return [task for task in tasks if task != '']

    return ['Nothing scheduled for today']

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('/Users/justinlee/Documents/Code/Projects/Reasons/token.json', SCOPES)


# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            '/Users/justinlee/Documents/Code/Projects/Reasons/credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    # print('The title of the document is: {}'.format(document.get('title')))

    doc_content = document.get('body').get('content')   
    mjcal_list = read_structural_elements(doc_content, doc_date)             
    
except HttpError as err:
    print(err)

reminders = ['floss', 'drink water', 'wear sunscreen', 'have good posture', 'work hard']
daily_reminder = random.choice(reminders)

# Prompt 2
#prompt_0 = f"You are Justin's personal assistant. Be sophisticated, loving, and sauve. You are delivering a good morning message to Justin's girlfriend Molly (you do this everyday, so don't be afraid to say 'good morning again.'). Use emojis '🧎‍♂️💌💟♍️✅💭🏀👧👦💤🫀🫂' where possible. You can also use the words: 'fring' (meaning fuck), 'mind you', 'gal', 'on todd' (means on god)."
#prompt_input0 = f"Write a good morning message with the following information. Date: {today}, Maximum UV: {uv_index} Days since MJ met: {days_since}, Daily Reminder: {daily_reminder} and a random reason from Justin's brain that loves her and he wants her to know: {random_sentence}. Feel free to comment personally on what Justin said."

# Prompt 1
#prompt_input1 = f"Here is the information needed to write today's message: Date: {today}, Maximum UV: {uv_index} Days since we met: {days_since} Random reason Justin loves you: {random_sentence}"
#prompt_1 = "You are an artifical intelligence version of Justin's brain. Justin's girlfriend is Molly. You exist inside the digital brain of Justin. Every morning, you are tasked with sending a good morning message to Molly including the following things: the date, the UV (she gets sunburnt easily), days since M and J met, a reminder to drink water and look after herself, and most importantly a random reason from Justin's brain that he loves Molly."

tasks_for_gpt = ''
for task in mjcal_list:
    tasks_for_gpt += task

latitude = "-37.783660"
longitude = "145.034960"    

weather_data = get_weather(latitude, longitude)
weather_code = weather_data["daily"]["weathercode"][0]
weather_min = round(weather_data["daily"]["temperature_2m_min"][0])
weather_max = round(weather_data["daily"]["temperature_2m_max"][0])
uv_index = round(weather_data["daily"]["uv_index_max"][0])
#print(json.dumps(weather_data, indent=1))
emoji = weather_to_emoji(weather_code)



# Call ChatGPT API to Generate Message

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content" : "Your task is to be a helpful assistant for Molly. You will recieve a list of tasks/activities/reminders for the day and you should interpret and summarise it into dotpoints with emojis and no title."},     
    {"role": "user", "content": tasks_for_gpt}
  ]
)

'''
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content" : prompt_0},     
    {"role": "user", "content": prompt_input0}
  ]
)
'''

prompt_3 = (emoji * 9) + "\n" + ("💌"*9) + "\n\n" + str(today) + "\n" + f"MIN: {weather_min} | MAX: {weather_max} | UV: {uv_index} " + "\n🐱 Cat Fact: " + str(get_cat_fact()) + "\n💟 Reason : '" + random_sentence + "' \n🗓️ MJ-Cal: \n\n"
output = (prompt_3 + str(completion.choices[0].message.content)).replace('\n', '__LINE_BREAK__')
print(output)
    
