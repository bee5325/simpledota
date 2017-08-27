import requests

class DotaRequest:

    base_url = "https://api.opendota.com/api"

    @staticmethod
    def get(field, args={}):

        url = ""
        response = None
        returnValue = ""

        if field == "win_count":
            url = "{base}/players/{player}/wl".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url)
            returnValue = response.json()['win']

        elif field == "win_rate_json":
            url = "{base}/players/{player}/wl?date={days}".format(base=DotaRequest.base_url, player=args['player'], days=args['days'])
            response = requests.get(url)
            returnValue = response.json()

        elif field == "win_rate":
            url = "{base}/players/{player}/wl".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url)
            winRate = response.json()["win"] * 100 / float(response.json()['win']+response.json()['lose'])
            returnValue = winRate

        elif field == "kills_count":
            url = "{base}/players/{player}/totals".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url)
            killsCount = [value['sum'] for value in response.json() if value['field']=='kills']
            returnValue = killsCount[0]

        elif field == "kda":
            url = "{base}/players/{player}/totals".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url)
            kda = [value['sum'] for value in response.json() if value['field']=='kda']
            returnValue = kda[0]

        elif field == "gold_per_min":
            url = "{base}/players/{player}/totals".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url)
            gpm = [value['sum'] for value in response.json() if value['field']=='gold_per_min']
            returnValue = gpm[0]

        elif field == "xp_per_min":
            url = "{base}/players/{player}/totals".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url)
            xpm = [value['sum'] for value in response.json() if value['field']=='xp_per_min']
            returnValue = xpm[0]

        elif field == "heroes":
            url = "{base}/heroes".format(base=DotaRequest.base_url)
            response = requests.get(url)
            returnValue = response.json()

        elif field == "heroes_used":
            url = "{base}/players/{player}/heroes".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url)
            returnValue = response.json()

        else:
            raise ValueError("{field} is not a valid request".format(field=field))

        if response.status_code != 200:
            raise IOError("Failed requests to get [{field}] with parameters [{param}]".format(field=field, param=args['player']))
        
        return returnValue


