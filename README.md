# IntroBot
Python Discord bot that will join members in a voice channel and play short intros

Requires >= python3.5

invite link:
https://discordapp.com/api/oauth2/authorize?client_id=CLIENT-ID-HERE&permissions=3147776&scope=bot

text permissions: send messages

voice permissions: connect, speak


## Configure
mkdir IntroBot && cd IntroBot

nano auth.json

{
"token": "BOT-TOKEN-HERE"
}

git clone https://github.com/collinxsmith1/IntroBot.git


cd IntroBot

pip install virtualenv

python3 -m venv env

source env/bin/activate

pip install -r requirements.txt

## Modify introbot.py
v_ids should be list of voice channel IDs that you want intros enabled in

tdelta is default at 3600 seconds

## Running

chmod +x introbot.py
python3 introbot.py
