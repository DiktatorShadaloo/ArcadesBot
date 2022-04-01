import configparser
import string
import requests
from pathlib import Path
import json
configFilePath = str(Path(__file__).parents[1]) + '/config/config.ini'

# allow_no_value permite keys sin valor, esto se utiliza para obtener la lista de mods.
configParser = configparser.RawConfigParser(allow_no_value=True)
# No permito la conversion a minusculas.
configParser.optionxform = lambda optionstr: optionstr
configParser.read(configFilePath)

def getChannelID( access_token, client_id):
    headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer %s' % (access_token)
    }
    response = requests.get('https://api.twitch.tv/helix/users', headers=headers)
    data = response.json()['data'][0]
    return int(data['id'])

def getReward_ID(channel_id, channel_token, client_id, reward_name):
    headers = {
    'Client-ID': client_id,
    'Authorization': 'Bearer %s' % (channel_token)
    }
    response = requests.get('https://api.twitch.tv/helix/channel_points/custom_rewards?broadcaster_id=%s'% (channel_id), headers=headers)
    data = response.json()['data']
    for x in data:
        if reward_name.lower() == x['title'].lower():
            return x['id']

BOT_NICK = configParser.get('BOT', 'bot_nick')
BOT_TOKEN = configParser.get('BOT', 'bot_token')
BOT_PREFIX = configParser.get('BOT', 'bot_prefix')
CHANNEL = [configParser.get('CHANNEL', 'channel_name')]
CHANNEL_TOKEN = configParser.get('CHANNEL', 'channel_token')
#CHANNEL_ID = int(configParser.get('CHANNEL', 'channel_id'))
CLIENT_ID = configParser.get('CHANNEL', 'client_id')
CHANNEL_ID = getChannelID(CHANNEL_TOKEN,CLIENT_ID)
REWARD_INSERT_COINS = configParser.get('CHANNEL', 'reward_insert_coins')
INSERT_COINS_ID = getReward_ID(CHANNEL_ID, CHANNEL_TOKEN,CLIENT_ID, REWARD_INSERT_COINS)
REWARD_BUY_COIN = configParser.get('CHANNEL', 'reward_buy_coin')
BUY_COIN_ID = getReward_ID(CHANNEL_ID, CHANNEL_TOKEN,CLIENT_ID, REWARD_BUY_COIN)
MODS = list(configParser['MODS'].keys())
PRECIO_BITS = int(configParser.get('CHANNEL', 'precio_bits'))
FICHAS_X_SUB = int(configParser.get('CHANNEL', 'fichas_x_sub'))
PRECIO_FICHA = float(configParser.get('CHANNEL', 'precio_ficha'))
FICHAS_MAXIMAS = int(configParser.get('CHANNEL', 'fichas_maximas'))
BANNED_MESSAGES = list(configParser['BANNED_MESSAGES'].keys())
AUTOMATIC_MESSAGES = list(configParser['AUTOMATIC_MESSAGES'].keys())