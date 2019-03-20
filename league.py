import datetime
import time
import requests

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
