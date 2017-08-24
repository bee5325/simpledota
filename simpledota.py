from datetime import datetime, timedelta

import dota2api

invalidID = "12443723"

class Simpledota:

    apikey = ""
    api = None
    instance = None

    def Initialise():
        Simpledota.apikey = "A18F4C9C87EAF1D8565A2D337049C764"
        Simpledota.api = dota2api.Initialise(Simpledota.apikey)

    #------------ functions
    def leaderboard(players, days):
        if len(players) == 0:
            return "Parameter 'player' is not provided"
        # get winrate for x days
        for player in players:
            winRates = Simpledota.getWinRate(player, days)
        # sort players
        leaderboard = Simpledota.sortPlayers(winRates)
        return leaderboard

    def suggest(players):
        p = Simpledota.getPlayer(players)
        return p

    def compare(players):
        if len(players) != 2:
            return "Error : Exactly 2 players are needed."
        else:
            validPlayerlist = []
            for player in players:
                p = Simpledota.getPlayer(players)
                validPlayerlist.append(p)
        return validPlayerlist

    #------------- helper functions
    def getWinRate(player, days):
        matches = Simpledota.getPlayerMatches(player, days)
        winRate = Simpledota.winRateForMatches(player, matches)
        return winRate

    def getPlayerMatches(player, days):

        timeRequired = datetime.today() - timedelta(days=days)
        requiredTimestamp = timeRequired.timestamp()
        # to cover for limitation of dota2api which can only get maximum of 100 matches per queries
        matchid = [requiredTimestamp]
        try:
            matchQueried = Simpledota.api.get_match_history(player)
        except dota2api.src.exceptions.APIError:
            return "Cannot access private account {}".format(player)
        if len(matchQueried["matches"]) == 0:
            raise Exception("Cannot get any match for player {}.".format(player))
        inTimeRange = True
        while True:
            for match in matchQueried["matches"]:
                if match["start_time"] >= requiredTimestamp:
                    matchid.append(match["match_id"])
                else:
                    inTimeRange = False
                    break
            if inTimeRange:
                matchQueried = Simpledota.api.get_match_history(player, start_at_match_id=matchid[-1])
                if (len(matchQueried["matches"]) == 1):
                    # no more entries in record, return what available
                    break
            else:
                break
        return matchid

    #########
    def winRateForMatches(player, matches):

        return (player, matches)

    #########
    def sortPlayers(winRates):
        return winRates

    def getPlayer(players):
        validPlayerlist = []
        validPlayerlist.append(Simpledota.api.get_player_summaries(players['idlist']))
        return validPlayerlist

