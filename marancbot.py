import telegram
from telegram.ext import Updater, CommandHandler
import logging
import requests
import re
import datetime
import time

LOL_TOKEN = 'RGAPI-466e04c4-af08-4e18-8324-ba7917b80612'

# Setup
bot = telegram.Bot(token='589572398:AAE-cO9K8mxK3zXW9uj0YExcSSSbF3WYUE0')
updater = Updater(token='589572398:AAE-cO9K8mxK3zXW9uj0YExcSSSbF3WYUE0')
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Ping command
def ping(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Pong")

ping_handler = CommandHandler("ping", ping)
dispatcher.add_handler(ping_handler)

# League user command
def ms_to_text(ms):
    d = ms // (3600 * 24 * 1000)
    ms = ms % (3600 * 24 * 1000)
    h = ms // (3600 * 1000)
    ms = ms % (3600 * 1000)
    m = ms // (60 * 1000)

    text = str(d).replace(".0","") + (" giorno, " if d == 1 else " giorni, ") + str(h).replace(".0","") + (" ora, " if h == 1 else " ore, ") + "e " + str(m).replace(".0","") + (" minuto" if m == 1 else " minuti")
    return text

def getLeagueInfo(bot, update, args):
    if(len(args) != 1):
        bot.send_message(chat_id=update.message.chat_id, parse_mode="Markdown", text="Looks up information about a player in EUW.\n\nUsage:\n\n`/league <username>`")
        return


    contents = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + args[0] + '?api_key=' + LOL_TOKEN).json()
    # Updates league version to look up for
    current_version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]
    match_data = requests.get('https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + contents['accountId'] + '?api_key=' + LOL_TOKEN).json()

    league_abstinence = (time.time() * 1000 - match_data['matches'][0]['timestamp'])
    icon = "http://ddragon.leagueoflegends.com/cdn/" + current_version + "/img/profileicon/" + str(contents['profileIconId']) + ".png"
    caption = "👨‍💻 *Username:* " + contents['name'] + "\n🤹‍♂️ *Summoner level:* " + str(contents['summonerLevel'])
    caption += "\n\n💉 *Grado di astinenza:* Non fa uso di LOL da " + ms_to_text(league_abstinence) +  ".\n🤼 *Match totali:* Ha giocato la bellezza di " + str(match_data['totalGames']) + " partite nella stagione corrente."
    bot.send_photo(chat_id=update.message.chat_id, photo=icon, caption=caption, parse_mode="Markdown")

league_handler = CommandHandler('league', getLeagueInfo, pass_args=True)
dispatcher.add_handler(league_handler)


updater.start_polling()
