# 🤖 J-GPT Personal Assistant for Justin and Molly 

<img src="https://github.com/jl33-ai/girlfriend-gpt-butler/assets/127172022/f64a8667-0226-4359-a88c-4f55f570cf07" width="50%">

This project aims to create a personalized daily message for Justin's girlfriend, using the GPT-3.5-turbo model from OpenAI. The message includes details such as the date, maximum UV index, days since they met, a daily reminder, and a random reason why Justin likes Molly. Additionally, it provides a summary of tasks/activities/reminders for the day from a Google Doc - automating their daily schedules in the process. 

### Features
- Retrieves daily UV index using OpenUV API.
- Fetches tasks and activities from a shared Google Doc (which serves as calendar)
- Fetches a single random line from an online 'reasons.txt' repository.
- Compiles this all into a personalized message using GPT-3.5-turbo.
- Includes emojis and unique phrases in the message.

`With the press of a button.`

### Dependencies

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

**Simple Automator Script to Deliver iMessage:**

```automator
on run {input, parameters}
	set theSentence to item 1 of input
	set phoneNumber to "0481369898" -- Replace with the recipient's phone number
	
	-- Replace the placeholder string back to line breaks before sending the message
	set theMessage to my replaceText(theSentence, "__LINE_BREAK__", return)
	
	tell application "Messages"
		set targetService to 1st account whose service type = iMessage
		set targetBuddy to participant phoneNumber of targetService
		send theMessage to targetBuddy
	end tell
end run

-- Function to replace text
on replaceText(textString, oldString, newString)
	set {tempTID, AppleScript's text item delimiters} to {AppleScript's text item delimiters, oldString}
	set textString to text items of textString
	set AppleScript's text item delimiters to newString
	set textString to "" & textString
	set AppleScript's text item delimiters to tempTID
	return textString
end replaceText
```
