# girlfriend-gpt-butler

J-GPT Personal Assistant for Justin and Molly

This project aims to create a personalized daily message for Molly, Justin's girlfriend, using the GPT-3.5-turbo model from OpenAI. The message includes details such as the date, maximum UV index, days since they met, a daily reminder, and a random reason why Justin loves Molly. Additionally, it provides a summary of tasks/activities/reminders for the day from a Google Doc.

Features

Retrieves daily UV index using OpenUV API.
Fetches tasks and activities from a shared Google Doc.
Generates a personalized message using GPT-3.5-turbo.
Includes emojis and unique phrases in the message.
Dependencies

Python 3.6+
google-auth
google-auth-oauthlib
google-auth-httplib2
google-api-python-client
requests
openai

*Of course, this is paired with your automation software of choice; personally, I used an automator script which was nicely integrated into the MacOS ecosystem, so a seamless scheduled delivery through iMessage was possible.*

**An example message:**

![Example Message](example_message.jpg)
