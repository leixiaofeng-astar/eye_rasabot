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
rase shell
```
