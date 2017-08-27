from datetime import datetime, timedelta
from operator import itemgetter 
from collections import OrderedDict
import json

from dotaRequest import *

class Leaderboard:

    response = dict()

    @staticmethod
    def leaderboard(players, days):
        if len(players) == 0:
            return "Parameter 'player' is not provided"
        allPlayers = Leaderboard.getWinRates(players, days)
        sortedPlayers = Leaderboard.sortPlayers(allPlayers)
        Leaderboard.response['days_queried'] = days
        Leaderboard.response['start_date'] = (datetime.today() - timedelta(days=days)).isoformat()
        Leaderboard.response['player_count'] = len(players)
        Leaderboard.response['players'] = sortedPlayers
        response = Leaderboard.formatResponse()
        return response

    @staticmethod
    def getWinRates(players, days):
        allPlayers = list()
        for player in players:
            match = DotaRequest.get("win_rate_json", {'player':player,'days':days})
            currentPlayer = dict()
            currentPlayer['player_id'] = player
            currentPlayer['match_count'] = match['win'] + match['lose']
            currentPlayer['win_num'] = match['win']
            currentPlayer['lose_num'] = match['lose']
            try:
                currentPlayer['win_rate'] = match['win']*100 / float(match['win']+match['lose'])
            except ZeroDivisionError:
                currentPlayer['win_rate'] = 0
            allPlayers.append(currentPlayer)
        return allPlayers

    @staticmethod
    def sortPlayers(players):
        sortedPlayers = sorted(players, key=itemgetter('win_rate'), reverse=True)
        ranking = 1
        for player in sortedPlayers:
            player['ranking'] = ranking
            ranking += 1
        return sortedPlayers 

    @staticmethod
    def formatResponse():
        formattedResponse = OrderedDict([
            ('days_queried', Leaderboard.response['days_queried']),
            ('start_date' , Leaderboard.response['start_date']),
            ('player_count', Leaderboard.response['player_count']),
            ('players', list(
                OrderedDict([
                    ('ranking', player['ranking']),
                    ('player_id', player['player_id']),
                    ('match_count', player['match_count']),
                    ('win_num', player['win_num']),
                    ('lose_num', player['lose_num']),
                    ('win_rate', player['win_rate'])
                ]) for player in Leaderboard.response['players'])
            )
        ])
        return json.dumps(formattedResponse)

if __name__== "__main__":
    print(Leaderboard.leaderboard([70388657, 91369376, 52191022], 7))
