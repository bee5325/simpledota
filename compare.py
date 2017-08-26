from datetime import datetime, timedelta
from time import mktime
from operator import itemgetter
import collections
import json
import requests

class Compare:

    @staticmethod
    def compare(players):
        if len(players) != 2:
            return "Error : Exactly 2 players are needed."
        else:
            validPlayerlist = players
        return validPlayerlist

if __name__== "__main__":
    print(Compare.compare([70388657, 91369376]))
