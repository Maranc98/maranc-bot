import random
import sys
import os
import math
from PIL import Image

pokemon_list = []
pokemon_families = []

pokemon_survival_rate = 0.3 # Probabilità che una famiglia di pokemon non sia dichiarata immigrato illegale nella nuova regione di Pokemon Spada-Scudo

image_width = 40
image_height = 30
max_pokemon_per_row = 10

with open('data/pokemon/pokemon_list.csv','r') as file:
    for line in file:
        pokemon_list.append(line.strip('\n').split(';'))

with open('data/pokemon/evolution_families.csv','r') as file:
    for line in file:
        family_string = line.strip('\n').split(';')
        family = []
        for pokemon in family_string:
            pokemon_entry = pokemon.strip('[').strip(']').split("', ")
            try:
                pokemon_entry[0] = pokemon_entry[0][1:]
                pokemon_entry[1] = pokemon_entry[1].strip("'").strip("\"")
            except:
                print(pokemon_entry)

            family.append(pokemon_entry)
        pokemon_families.append(family)

number_of_families_allowed = int(len(pokemon_families) * pokemon_survival_rate)

def sorting_function(family):
    key = 10000
    for pokemon in family:
        if float(pokemon[0]) < key:
            key = float(pokemon[0])
    return key

async def legal_decree(update, bot):
    legal_pokemon_families = random.sample(pokemon_families, number_of_families_allowed)
    legal_pokemon_families = sorted(legal_pokemon_families, key = sorting_function)

    paths = []

    for family in legal_pokemon_families:
        for pokemon in family:
            paths.append('data/pokemon/icons/' + str(int(float(pokemon[0]))) + '.png')

    images = [Image.open(i) for i in paths]
    images_ordered = []
    final_image = Image.new('RGBA', (image_width * max_pokemon_per_row, image_height * math.ceil(len(images)/max_pokemon_per_row)), color=(255,255,255))
    for i in range(int(len(images)/max_pokemon_per_row)):
        for j in range(max_pokemon_per_row):
            final_image.paste(images[i*max_pokemon_per_row+j],(j*image_width,i*image_height))

    try:
        os.remove('data/pokemon/XD.png')
    except:
        pass

    final_image.save('data/pokemon/XD.png')

    photo = await bot.send_photo(chat_id = update['chat']['id'],
                                photo = open('data/pokemon/XD.png', 'rb'))
    await bot.sendMessage(chat_id = update['chat']['id'],text = "Come dichiarato dal ministro dell'Interno, Junichi Masuda,🙏👼 secondo le indiscrezioni circolate nelle ultime 48 ore ⏰,  il decreto già ribattezzato \"Gotta catch some of them\" 😂😂 ha come principale obiettivo quello di tutelare il lavoro 👨‍🔧👨‍🚒 delle forze dell'ordine impegnate sul territorio di Galar 👮‍♀️, inasprire le pene per il reato di immigrazione clandestina. ⚖️🚨 Questi sono un esempio dei pokemon, 30% del totale 😱, che potrebbero sopravvivere alla strage... 😠😠😔 Cioffi perde 1v1 con seba, ragequitta da league e evade le tasse uwu ochinchin daisuki 🍆")
    return photo
