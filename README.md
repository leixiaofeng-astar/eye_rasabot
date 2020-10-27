# eye_rasabot: Implementing patient actions with backend integrations, forms and fallback

---
## What's in this bot?

In this bot we:
- the NLU data of our assistant by adding more training examples, implementing regex features and synonyms
- updated the custom action with eye data
- implemented form action

## How do I use this directory?
Train the assistant using the command:  
`rasa train`

Test the assistant using the command:  
`rasa run actions & rasa shell`

## What do you need to follow this bot?

This bot requires you to have Rasa installed on your machine:  
```pip3 install rasa-x --extra-index-url https://pypi.rasa.com/simple```

The commands to train and run the built model:  
```
rasa train core
rasa train nlu
rasa shell nlu
rasa run actions
rasa shell
```

The commands to run conversation on telegram bot:  
download and install ngrok from https://ngrok.com/download
example in mac PC as below
```
brew cask install ngrok
ngrok http 5005
```
copy the link after running ngrok
(such as "Forwarding https://aaf2706626d2.ngrok.io -> http://localhost:5005" ) 
to credentials.yml
webhook_url: "https://aaf2706626d2.ngrok.io/webhooks/telegram/webhook"
then run the command
```
rasa run --debug
```