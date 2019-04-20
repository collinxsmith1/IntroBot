# IntroBot
Python Discord bot that will join members in a voice channel and play short intros

## Capabilities
Capable of handling multiple guilds
Upload your own .mp3 file to be your intro
Change your intro volume
Reset your intro timer

## Prerequisites
Requires >= python3.5

invite link:
https://discordapp.com/api/oauth2/authorize?client_id=CLIENT-ID-HERE&permissions=3147776&scope=bot

text permissions: send messages

voice permissions: connect, speak

## Install
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

## Configure introbot.py for your discord servers
v_ids should be list of voice channel IDs that you want intros enabled in

tdelta is default at 3600 seconds (this avoids spamming of intros)

## Running bot
chmod +x introbot.py

python3 introbot.py

## Future ideas
More administration powers to certain guild roles
Certain guild roles would be capable of giving individual members temporary bans from their intros
Certain guild roles would be capable of enabling or disabling intros for voice channels
