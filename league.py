import datetime
import time
import requests
import re

from tokens import LOL_TOKEN
from utils import ms_to_text

async def league(update, bot):
    text = update['text'].split(' ')
    chat_id = update['chat']['id']
    if(len(text) < 2):
        return dict(
            text = "Looks up information about a player in EUW.\n\nUsage:\n\n`/league <username>`",
            parse_mode = "Markdown"
        )

    username = text[1]

    # League API requests
    contents = requests.get('https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/' + username + '?api_key=' + LOL_TOKEN).json()
    current_version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]
    match_data = requests.get('https://euw1.api.riotgames.com/lol/match/v4/matchlists/by-account/' + contents['accountId'] + '?api_key=' + LOL_TOKEN).json()

    league_abstinence = await ms_to_text(time.time() * 1000 - match_data['matches'][0]['timestamp'])
    icon = "http://ddragon.leagueoflegends.com/cdn/" + current_version + "/img/profileicon/" + str(contents['profileIconId']) + ".png"
    caption = "👨‍💻 *Username:* " + contents['name'] + "\n🤹‍♂️ *Summoner level:* " + str(contents['summonerLevel'])
    caption += "\n\n💉 *Grado di astinenza:* Non fa uso di LOL da " + league_abstinence +  ".\n🤼 *Match totali:* Ha giocato la bellezza di " + str(match_data['totalGames']) + " partite nella stagione corrente."

    return await bot.sendPhoto(
        chat_id = chat_id,
        caption = caption,
        photo = icon,
        parse_mode="Markdown"
    )

async def settoken(update, bot):
    new_token = update['text'].split(' ')


    if(len(new_token) < 2):
        return "You have to write a token for this to work! .. Or were you trying to take my precious key? 😠"

    new_token = new_token[1]
    words = re.split('-',new_token)

    if(len(new_token) != 42 or
       len(words) != 6 or
       len(words[0]) != 5 or
       len(re.findall('[a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z][a-zA-Z]',words[0])) != 1 or
       len(words[1]) != 8 or
       len(re.findall('[a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9]',words[1])) != 1 or
       len(words[2]) != 4 or
       len(words[3]) != 4 or
       len(words[4]) != 4 or
       len(re.findall('[a-z0-9][a-z0-9][a-z0-9][a-z0-9]',words[2])) != 1 or
       len(re.findall('[a-z0-9][a-z0-9][a-z0-9][a-z0-9]',words[3])) != 1 or
       len(re.findall('[a-z0-9][a-z0-9][a-z0-9][a-z0-9]',words[4])) != 1 or
       len(words[5]) != 12 or
       len(re.findall('[a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9][a-z0-9]',words[5])) != 1
       ):
       monkas = open('badppl.csv','a')
       date = update['date']
       text = update['text']

       #sistemare, e' un po' bruttino
       if 'from' in update:
           sender = update['from']
           if 'username' in sender:
               username = sender['username']
           else:
               username = 'None'

           if 'last_name' in sender:
               last_name = sender['last_name']
           else:
               last_name = 'None'
       else:
           sender = {'first_name' : 'None', 'is_bot' : 'None', 'id' : 'None'}
           last_name = 'None'
           username = 'None'


       monkas.write(sender['first_name'] + ',' + last_name + ',' + username + ',' + str(sender['is_bot']) + ',' + str(sender['id']) + ',' + str(date) + ',' + text + '\n')
       monkas.close()
       return "You have just set LOL_TOKEN to " + new_token + ". Restart the bot to start using the new token!"

    tokens_file = open('tokens.py', 'r')
    text = tokens_file.read()
    tokens_file.close()

    tokens_file = open('tokens.py', 'w')
    text = text.replace(text[73:115],new_token)
    tokens_file.write(text)
    tokens_file.close()

    return "You have just set LOL_TOKEN to " + new_token + ". Restart the bot to start using the new token!"
