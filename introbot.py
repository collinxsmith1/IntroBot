#!/usr/bin/env python3

# Discord bot for voice channel intro tunes
# Migrated for discord.py module v1.0.1

import discord
import json
import asyncio
import time
import os

import aiohttp
import socket
import aiofiles 

path = os.getcwd()

with open(os.path.join(path,'../auth.json')) as auth:
    secret = json.loads(auth.read())
    
client = discord.Client()

def RepresentsFloat(s):
    try: 
        float(s)
        return True
    except ValueError:
        return False

@client.event
async def on_ready():
    print('Logged in as')
    print('bot: ' + client.user.name)
    print('user ID: ' + str(client.user.id))
    print('active servers: ')
    for guild in client.guilds:
        print(guild)
        print('    channels: ')
        for channel in guild.channels:
            print('        ' + str(channel))
    print('-------')

    action = discord.Game('Intros')
    await client.change_presence(status=discord.Status.online, activity=action, afk=False)

if not os.path.exists(os.path.join(path,'introdata')):
    os.makedirs(os.path.join(path,'introdata'))

@client.event
async def on_voice_state_update(member, before, after):

    ### ANY CHANNEL Intro Tunes ###

    if not member.bot: # disregards any bots
        if before.self_deaf == after.self_deaf: # stops if member toggled deafen
            if before.self_mute == after.self_mute: # stops if member toggled mute
                if not after.channel == None: # stops if member left a voicechannel
                    vchanid = after.channel.id
                    v_ids = [] # Add voicechannel IDs to this list to enable them for the intro

                    if vchanid in v_ids:
                        intpath = os.path.join(path, 'introdata/')
                        intuser = os.path.join(intpath, str(member))
                        inttime = intuser + '_time.txt'
                        intvol = intuser + '_volume.txt'
                        intmp3 = intuser + '.mp3'
                        defaultmp3 = intpath + '/defaultintro.mp3' # saving filepaths for user data

                        itime = time.time() # time of intro
                        
                        if os.path.exists(inttime):
                            with open(inttime, "r") as bf: # reading from existing user time data
                                tdata = bf.read()
                            if tdata == '':
                                tdata = 0 # buddyintrotime has no information so tdata resorts to 0
                        else:
                            with open(inttime, "w") as bf: # write new user time data
                                bf.write(str(itime))
                            tdata = 0 # buddyintrotime didnt exist so tdata resorts to 0

                        if os.path.exists(intvol):
                            with open(intvol, "r") as rv: # reading from existing user volume data
                                voldata = rv.read()
                                voldata = float(voldata)
                            if voldata == '':
                                voldata = 0.25 # default intro volume
                        else:
                            voldata = 0.25 # default intro volume is 25%
                            
                        if os.path.exists(intmp3): # plays existing user intro mp3
                            mp3file = intmp3
                        else:
                            mp3file = defaultmp3 # if no user intro, plays the default tune
                            
                        tdelta = 3600 # time threshold in seconds since users last intro
                        readtime = itime - float(tdata)
                        if tdelta <= readtime: # time threshold logic
                            vc = await after.channel.connect()
                            mp3source = discord.FFmpegPCMAudio(mp3file)
                            mp3sourcetrans = discord.PCMVolumeTransformer(mp3source)
                            mp3sourcetrans.volume = voldata
                            vc.play(mp3sourcetrans)

                            while vc.is_playing():
                                await asyncio.sleep(1)
                            vc.stop()
                            await vc.disconnect()
                            print('yes intro of:', str(member))
                            
                            with open(inttime, "w") as bf:
                                bf.write(str(itime))
                        else:
                            print(' no intro of:', str(member))
    
functionlist = ['~~~~~ IntroBot functions: ~~~~~',
                '!patchnotes : see latest bot patchnotes',
                '!rit : reset your intro timer (timer is set to 10 seconds for testing)',
                '!changeintro : add .mp3 as message attachment to change your intro tune',
                '!introvolume x : x = [0 < x <= 2.0] to change your intro volume (default = 0.25)'
                ]
    
patchlist = ["v0.9 (20190418): Multi voice channel enabled, add your own intro .mp3, change it's volume, I'll play your anthem when you join",
             "v1.0 (20190419): Migrated to discord.py v1.0.1"
            ]

@client.event
async def on_message(message):
    
    if message.content == '!patchnotes':
        patchmsg = "```"
        for patch in patchlist:
            patchmsg += patch + '\n'
        patchmsg += "```"
        await message.channel.send(patchmsg)
    
    if message.content == '!PatrickBot': # Change to name of the Bot using this script
        funcmsg = "```"
        for function in functionlist:
            funcmsg += function + '\n'
        funcmsg += "```"
        await message.channel.send(funcmsg)
        
    if message.content == '!rit': # deletes message author's time file to reset their intro timer
        mAuthor = str(message.author)
        buddyfile = path + '/introdata/' + mAuthor + '_time.txt'
        if os.path.exists(buddyfile):
            print('time file removed:', buddyfile)
            os.remove(buddyfile)

    if message.content.startswith('!introvolume'): # overwrites message author's volume file with message argument (float between 0 and 2)
        mAuthor = str(message.author)
        buddyfile = path + '/introdata/' + mAuthor + '_volume.txt'
        msgsplit = message.content.split()
        if len(msgsplit) == 2:
            volint = msgsplit[1]
            if RepresentsFloat(volint):
                volint = float(volint)
                
                if 0 < volint <= 2:
                    if os.path.exists(buddyfile):
                        with open(buddyfile, "w") as vf:
                            vf.write(str(volint))
                        await message.channel.send('Changed volume of ' + mAuthor + ' to {} '.format(str(volint)))
                    else:
                        with open(buddyfile, "w") as vf:
                            vf.write(str(volint))
                        await message.channel.send('Created new volume file for ' + mAuthor + ' to {} '.format(str(volint)))
                    print('intro volume file of:', mAuthor, 'changed to:', str(volint))
                else:
                    await message.channel.send('Try a value between [0 - 2.0]')
            else:
                await message.channel.send('Try a real number [0 - 2.0]')
        else:
            await message.channel.send('Try with one number after a space [0 - 2.0]')
    
    
    if message.content.startswith('!changeintro'): # changes message author's intro file .mp3 to message attachment (.mp3 < 300 KB)
        mAuthor = str(message.author)
        attachment = message.attachments
        mp3filesize = attachment[0].size
        mp3filename = attachment[0].url

        async with aiohttp.ClientSession() as session:
            if mp3filename.endswith('.mp3'):
                if mp3filesize <= 300000:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(mp3filename) as resp:
                            if resp.status == 200:
                                f = await aiofiles.open(path + '/introdata/' + mAuthor + '.mp3', mode='wb')
                                await f.write(await resp.read())
                                await f.close()
                    await session.close()
                    print('changed intro of:', mAuthor, 'to:', str(mp3filename))
                    await message.channel.send('Changed intro of ' + mAuthor + ' to hopefully something not cancerous')
                else:
                    await message.channel.send('Try a smaller filesize there bud. < 300 KB please')
            else:
                await message.channel.send("Try an actual mp3 file there bud. It ends in '.mp3'")
            
client.run(secret["token"])

