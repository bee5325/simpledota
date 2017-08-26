from dotaRequest import *

class Heroes:

    heroes = list()
    roles = dict()

    @staticmethod
    def initialise():
        allheroes = DotaRequest.get("heroes")
        Heroes.heroes = Heroes.simplifiedHerolist(allheroes)
        Heroes.roles = Heroes.heroesByRoles(allheroes)

    @staticmethod
    def simplifiedHerolist(allheroes):
        # some id are missing, don't use simple loop directly to assign to list
        lastId = allheroes[-1]['id']
        simplifiedlist = dict()
        for hero in allheroes:
            simplifiedlist[hero['id']] = dict()
            simplifiedlist[hero['id']]['id'] = hero['id']
            simplifiedlist[hero['id']]['name'] = hero['localized_name']
            simplifiedlist[hero['id']]['roles'] = hero['roles']
        return simplifiedlist

    @staticmethod
    def heroesByRoles(allheroes):
        roleDict = dict()
        for hero in allheroes:
            for role in hero['roles']:
                if role in roleDict:
                    roleDict[role].append(hero['localized_name'])
                else:
                    roleDict[role] = [hero['localized_name']]
        return roleDict

if __name__ == "__main__":
    print(Heroes.initialise())
