# bot.py
import os
import random
import discord
from dotenv import load_dotenv
import logging
import os, sys, subprocess, shlex, re
from subprocess import call

# 1
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    
image_types = ["png", "jpeg", "gif", "jpg", "mp4", "mp3"]

@bot.event
async def on_message(Message):
    print(Message.attachments)
    for attachment in Message.attachments:
        if any(attachment.filename.lower().endswith(image) for image in image_types):
            await attachment.save(attachment.filename)
            if (probe_file(attachment.filename) == True):
            	print("NIELEGALNY PLIK")
            	await Message.delete()
            	channel = Message.channel
            	await channel.send("Przepraszamy, plik, który wrzuciłeś/aś, był prawdopodobnie niebezpieczny i został automatycznie usunięty.")
            else:
            	print("Bezpieczny plik")
    
#3

def probe_file(filename):
    cmnd = ['ffprobe', '-v', 'error', '-show_entries', 'frame=width,height', '-select_streams', 'v', '-of', 'csv=p=0', filename]
    p = subprocess.Popen(cmnd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(filename)

    lines = []

    while True:
        line = p.stdout.readline()
        if not line:
            break
        #the real code does filtering here
        lines.append(line.decode('utf-8').rstrip('/n'))

    for number, line in enumerate(lines):
        if number > 1:
            if lines[number] != lines[number - 1]:
                return True
    
    return False

#==========================================================================
bot.run(TOKEN)

