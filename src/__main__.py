from src.bot import main_BOT as bot
from src.client import main_CLIENT as client
from src.irc import main_IRC as irc
from multiprocessing import Process

if __name__ == "__main__":
    p1 = Process(target = bot)
    p1.start()
    p2 = Process(target = client)
    p2.start()
    p3 = Process(target = irc)
    p3.start()