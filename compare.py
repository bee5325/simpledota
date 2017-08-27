from collections import OrderedDict
import json

from dotaRequest import *

class Compare:

    DEFAULT_ATTRIBUTE = "win_count"

    response = {}

    @staticmethod
    def compare(players, attribute=None):
        if len(players) != 2:
            return "Error : Exactly 2 players are needed."
        if attribute is None:
            attribute = Compare.DEFAULT_ATTRIBUTE

        Compare.response['attribute'] = attribute
        try:
            playersAttribute = Compare.getAttribute(players, attribute)
        except ValueError as e:
            return "{attribute} is not a valid attribute for compare".format(attribute=attribute)
        except IOError:
            return e
        Compare.compareByAttribute(playersAttribute)
        result = Compare.formatResponse()
        return result

    def getAttribute(players, attribute):
        playerAttribute = dict()
        try:
            for player in players:
                playerAttribute[player] = DotaRequest.get(attribute, {'player' : player})
        except (ValueError, IOError):
            raise
        return playerAttribute

    def compareByAttribute(playersAttribute):
        print(playersAttribute)
        players = list(playersAttribute.keys())
        if playersAttribute[players[0]] > playersAttribute[players[1]]:
            winner = 0
            other = 1
        else:
            winner = 1
            other = 0
        winnerDict = {
            'player_id' : players[winner],
            'score' : playersAttribute[players[winner]]
        }
        print(players[winner])
        print(playersAttribute[players[winner]])
        otherDict = {
            'player_id' : players[other],
            'score' : playersAttribute[players[other]]
        }
        Compare.response['winner'] = winnerDict
        Compare.response['other'] = otherDict

    def formatResponse():
        formattedResponse = OrderedDict([
            ('attribute',  Compare.response['attribute']),
            ('winner', OrderedDict([
                ('player_id', Compare.response['winner']['player_id']),
                ('score', Compare.response['winner']['score'])
            ])),
            ('other', OrderedDict([
                ('player_id', Compare.response['other']['player_id']),
                ('score', Compare.response['other']['score'])
            ]))
        ])
        return json.dumps(formattedResponse)

if __name__== "__main__":
    print(Compare.compare([70388657, 91369376]))
