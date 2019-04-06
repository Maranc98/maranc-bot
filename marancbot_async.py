import asyncio
from davtelepot import Bot
import logging
#import requests
#import re
import datetime
import time
import sys

from tokens import BOT_TOKEN
import utils
import league

# Setup
bot = Bot.get(BOT_TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Useful bot commands
@bot.command(command='/ping')
async def ping(update):
    return 'Pong'

@bot.command(command='/restart')
async def restart_command(update):
    bot.restart_bots()
    return 'I bot verranno riavviati entro 10 secondi.'

@bot.command(command='/update')
async def update_command(update):
    Bot.stop = 'Update'
    return 'Inizio l\'update del bot, brb.'

@bot.command(command='/ip')
async def ip_command(update):
    if(not utils.isAdmin(update)):
        return 'Not enough permissions.'
    return await utils.getIP()

# League
@bot.command(command='/league', descr='Ricerca informazioni su un giocatore.')
async def league_command(update):
    return await league.league(update, bot)

@bot.command(command='/settoken', descr='Setta il token dell\'API di LOL')
async def league_token(update):
    return await league.settoken(update, bot)

Bot.run()

# La .get() se non trova Bot.stop, restituisce 60

EXIT_RESULTS = {'Restart' : 65, 'Update' : 66, 'Notfound' : 60}
sys.exit(EXIT_RESULTS.get(Bot.stop,60))
