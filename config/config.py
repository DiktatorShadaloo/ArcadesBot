import configparser
from pathlib import Path

configFilePath = str(Path(__file__).parents[1]) + '/config/config.ini'

# allow_no_value permite keys sin valor, esto se utiliza para obtener la lista de mods.
configParser = configparser.RawConfigParser(allow_no_value=True)
# No permito la conversion a minusculas.
configParser.optionxform = lambda optionstr: optionstr
configParser.read(configFilePath)

BOT_NICK = configParser.get('BOT', 'bot_nick')
BOT_TOKEN = configParser.get('BOT', 'bot_token')
BOT_PREFIX = configParser.get('BOT', 'bot_prefix')
CHANNEL = [configParser.get('CHANNEL', 'channel_name')]
CHANNEL_TOKEN = configParser.get('CHANNEL', 'channel_token')
CHANNEL_ID = int(configParser.get('CHANNEL', 'channel_id'))
REWARD_NAME = configParser.get('CHANNEL', 'reward_name')
MODS = list(configParser['MODS'].keys())
PRECIO_BITS = int(configParser.get('CHANNEL', 'precio_bits'))
FICHAS_X_SUB = int(configParser.get('CHANNEL', 'fichas_x_sub'))
PRECIO_FICHA = float(configParser.get('CHANNEL', 'precio_ficha'))
FICHAS_MAXIMAS = int(configParser.get('CHANNEL', 'fichas_maximas'))
BANNED_MESSAGES = list(configParser['BANNED_MESSAGES'].keys())
