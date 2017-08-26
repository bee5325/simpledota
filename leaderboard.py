from datetime import datetime, timedelta
from time import mktime
from operator import itemgetter
import collections
import json
import requests

class Leaderboard:

    @staticmethod
    def leaderboard(players, days):
        if len(players) == 0:
            return "Parameter 'player' is not provided"
        # get winrate for x days
        allPlayers = list()
        for player in players:
            match = Leaderboard.getWinLose(player, days)
            currentPlayer = collections.OrderedDict()
            currentPlayer['player_id'] = player
            currentPlayer['match_count'] = match['win'] + match['lose']
            currentPlayer['win_num'] = match['win']
            currentPlayer['lose_num'] = match['lose']
            currentPlayer['win_rate'] = match['win']*100 / float(match['win']+match['lose'])
            allPlayers.append(currentPlayer)
        # sort players
        sortedPlayers = Leaderboard.sortPlayers(allPlayers)
        additionalInfo = Leaderboard.getAdditionalInfo(players, days)
        response = Leaderboard.formatResponse(sortedPlayers, additionalInfo)
        return response

    @staticmethod
    def getWinLose(player, days):
        matchRequest = requests.get("https://api.opendota.com/api/players/" + str(player) + "/wl?date=" + str(days))
        match = matchRequest.json()
        return match

    @staticmethod
    def sortPlayers(players):
        sortedPlayers = sorted(players, key=itemgetter('win_rate'), reverse=True)
        ranking = 1
        for player in sortedPlayers:
            player['ranking'] = ranking
            ranking += 1
        return sortedPlayers 

    @staticmethod
    def getAdditionalInfo(players, days):
        info = collections.OrderedDict()
        info['days_queried'] = days
        info['start_date'] = (datetime.today() - timedelta(days=days)).isoformat()
        info['player_count'] = len(players)
        return info

    @staticmethod
    def formatResponse(sortedPlayers, additionalInfo):
        response = additionalInfo
        response['players'] = sortedPlayers
        jsonResponse = json.dumps(response, sort_keys=False)
        return jsonResponse

if __name__== "__main__":
    print(Leaderboard.leaderboard([70388657, 91369376, 52191022], 7))
