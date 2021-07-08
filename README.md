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
Note: recommend rasa 2.x version for new training data format
```
pip3 install -U pip
pip3 install rasa
pip3 install rasa[transformers]
pip3 freeze | grep rasa
rasa==2.1.3
rasa-core==0.14.5
rasa-core-sdk==0.14.0
rasa-nlu==0.15.1
rasa-sdk==2.1.2
rasa-x==0.32.2
```
The exact rasa version as above was used in the test.

The commands which can be used to train and run the built model:  
```
rasa train core
rasa train nlu
rasa shell nlu
rasa run actions
rasa shell
```

## The commands to run conversation on telegram bot:  
download and install ngrok from https://ngrok.com/download
One example in mac PC as below
```
brew cask install ngrok
ngrok http 5005
```
One example in linux PC as below
```
sudo apt update
sudo apt install snapd
sudo snap install ngrok
ngrok http 5005
```
copy the link after running ngrok
(such as "Forwarding https://aaf2706626d2.ngrok.io -> http://localhost:5005") 
to credentials.yml file:  
webhook_url: "https://aaf2706626d2.ngrok.io/webhooks/telegram/webhook"
then run the command on the terminal:
```
rasa train
rasa run actions & rasa run --debug
```
then join the telegram bot which was configured in credentials.yml, and test the conversation ...

## Support - Bug Shooting
When the error message show:  
OSError: [Errno 48] error while attempting to bind on address ('0.0.0.0', 5055): address already in use
Please run
`sudo lsof -i tcp:5005`
to check which process is using the 5005 port, then use 
`sudo kill -9 XXXX`
to kill the process (Note: XXXX is the process ID)

When the question enter in telegram bot has not response:  
Please check the log info in the terminals which run "rasa run actions" and "rasa run --debug" for the details.
Then fix the error and re-run the rasa bot as "The commands to run conversation on telegram bot"

When the error "AttributeError: 'NoneType' object has no attribute 'text'" happened, please refer to
https://forum.rasa.com/t/telegram-error-exception-occurred-while-handling-uri/26407
Basically it seems that Rasa Telegram connector is not handling the Updates properly.

After run "ngrok http 5005", it has 8 hours limitation. Once 8 hours passed, it will show
"Session Expired Restart ngrok or upgrade: ngrok.com/upgrade" in red font.
Reason of Session Expires – ngrok limits your sessions to eight hours on the free version. You can register yourself and connect your account to ngrok app with command `./ngrok authtoken XXXXXX`
More info can refer to https://dashboard.ngrok.com/get-started/setup 
