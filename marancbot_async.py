import asyncio
from davtelepot import Bot
import logging
import datetime
import time
import sys
import os

from tokens import BOT_TOKEN
import utils
import league
import activities
import pokememe

import sqlite3
db_connection = sqlite3.connect('data/maranc-bot.db'.format(os.path.dirname(__file__)))

# Setup
bot = Bot.get(BOT_TOKEN)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Useful bot commands
@bot.command(command='/ping')
async def ping(update):
    return 'Pong'

@bot.command(command='/restart')
async def restart_command(update):
    if(not await utils.isAdmin(update)):
        return 'Not enough permissions.'
    bot.restart_bots()
    return 'I bot verranno riavviati entro 10 secondi.'

@bot.command(command='/update')
async def update_command(update):
    if(not await utils.isAdmin(update)):
        return 'Not enough permissions.'
    Bot.stop = 'Update'
    return 'Inizio l\'update del bot, brb.'

@bot.command(command='/ip')
async def ip_command(update):
    if(not await utils.isAdmin(update)):
        return 'Not enough permissions.'
    return await utils.getIP()

# League
@bot.command(command='/league', descr='Ricerca informazioni su un giocatore.')
async def league_command(update):
    return await league.league(update, bot)

@bot.command(command='/settoken', descr='Setta il token dell\'API di LOL')
async def league_token(update):
    return await league.settoken(update, bot)

# Activities
@bot.command(command='/act', descr='Aggiungi un\'attività')
async def activity_command(update):
    return await activities.add_activity(db_connection, update)

@bot.command(command='/mood', descr='Aggiungi un mood')
async def mood_command(update):
    return await activities.add_mood(db_connection, update)

@bot.command(command='/db', descr='Get database')
async def db_command(update):
    if(not await utils.isAdmin(update)):
        return 'Not enough permissions.'
    return await activities.get_db(update, bot)

# Pokememe
@bot.command(command='/feraligator', descr='Simula l\'imminente strage nel mondo dei Pokèmon')
async def pokememe_command(update):
    await pokememe.legal_decree(update, bot)

Bot.run()

# Spegnimento Bot

db_connection.close()

# La .get() se non trova Bot.stop, restituisce 60

EXIT_RESULTS = {'Restart' : 65, 'Update' : 66, 'Notfound' : 60}
sys.exit(EXIT_RESULTS.get(Bot.stop,60))
