from operator import itemgetter
from collections import Counter, OrderedDict
import json

from dotaRequest import *
from heroes import *

class Suggest:

    response = dict()

    @staticmethod
    def suggest(players):
        if len(players) != 1:
            return "Exactly one player is required."
        player = players[0]
        Suggest.response['player_id'] = player
        Heroes.initialise()
        heroesUsed = DotaRequest.get("heroes_used", {'player' : player})
        outstandingHeroes = Suggest.getOutstandingHeroes(heroesUsed)
        outstandingRoles = Suggest.getOutstandingRoles(outstandingHeroes)
        Suggest.suggestHeroes(outstandingRoles)
        formattedResponse = Suggest.formatResponse()
        return formattedResponse

    @staticmethod
    def getOutstandingHeroes(heroesUsed):
        winRate = list()
        for hero in heroesUsed:
            # only consider valid result if played more than 10 times
            if hero['games'] >= 10:
                winRate.append( (int(hero['hero_id']), hero['win']/float(hero['games'])) )
        sortedWinRate = sorted(winRate, key=itemgetter(1), reverse=True)
        # get only hero id, discard win rate
        strongestHeroes = [sortedWinRate[i][0] for i in range(5)]
        weakestHeroes = [sortedWinRate[i][0] for i in range(-1,-6,-1)]
        outstandingHeroes = {'strong' : strongestHeroes, 'weak' : weakestHeroes}
        Suggest.response['strongest_heroes'] = [Heroes.heroes[hero]['name'] for hero in strongestHeroes]
        Suggest.response['weakest_heroes'] = [Heroes.heroes[hero]['name'] for hero in weakestHeroes]
        return outstandingHeroes

    @staticmethod
    def getOutstandingRoles(outstandingHeroes):
        strongCounter = Counter()
        weakCounter = Counter()
        for heroId in outstandingHeroes['strong']:
            strongCounter += Counter(Heroes.heroes[heroId]['roles'])
        for heroId in outstandingHeroes['weak']:
            weakCounter += Counter(Heroes.heroes[heroId]['roles'])
        Suggest.response['strongest_roles'] = [x[0] for x in strongCounter.most_common()]
        Suggest.response['weakest_roles'] = [x[0] for x in weakCounter.most_common()]
        return { 'strong' : strongCounter, 'weak' : weakCounter }
        
    @staticmethod
    def suggestHeroes(outstandingRoles):
        strongHiScore = 0
        strongSuggest = 0
        weakHiScore = 0
        weakSuggest = 0
        for hero in Heroes.heroes.values():
            scores = Suggest.getHeroScore(hero, outstandingRoles)
            if scores['strong'] > strongHiScore:
                strongHiScore = scores['strong']
                strongSuggest = hero['id']
            if scores['weak'] > weakHiScore:
                weakHiScore = scores['weak']
                weakSuggest = hero['id']
        Suggest.response['strong_suggest'] = Heroes.heroes[strongSuggest]['name']
        Suggest.response['weak_suggest'] = Heroes.heroes[weakSuggest]['name']
        
    @staticmethod
    def getHeroScore(hero, outstandingRoles):
        strongScore = 0
        weakScore = 0
        for role in hero['roles']:
            strongScore += outstandingRoles['strong'][role]
            weakScore += outstandingRoles['weak'][role]
        return { 'strong' : strongScore, 'weak' : weakScore }

    @staticmethod
    def formatResponse():
        formattedResponse = OrderedDict([
            ('player_id', Suggest.response['player_id']),
            ('strongest_heroes', Suggest.response['strongest_heroes']),
            ('strongest_roles', Suggest.response['strongest_roles']),
            ('strong_hero_suggest', Suggest.response['strong_suggest']),
            ('weakest_heroes', Suggest.response['weakest_heroes']),
            ('weakest_roles', Suggest.response['weakest_roles']),
            ('weak_hero_suggest', Suggest.response['weak_suggest'])
        ])
        return json.dumps(formattedResponse)

if __name__== "__main__":
    print(Suggest.suggest([70388657]))
