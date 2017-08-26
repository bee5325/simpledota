import requests

class DotaRequest:

    base_url = "https://api.opendota.com/api/players"

    @staticmethod
    def get(field, args={}):

        if field == "win_count":
            url = "{base}/{player}/wl".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url).json()
            return response['win']

        elif field == "win_rate_json":
            url = "{base}/{player}/wl?date={date}".format(base=DotaRequest.base_url, player=args['player'], date=args['date'])
            response = requests.get(url).json()
            return response

        elif field == "win_rate":
            url = "{base}/{player}/wl".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url).json()
            winRate = response["win"] * 100 / float(response['win']+response['lose'])
            return winRate

        elif field == "kills_count":
            url = "{base}/{player}/totals".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url).json()
            killsCount = (value['sum'] for value in response if value['field']=='kills')
            return killsCount

        elif field == "kda":
            url = "{base}/{player}/totals".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url).json()
            kda = (value['sum'] for value in response if value['field']=='kda')
            return kda

        elif field == "gold_per_min":
            url = "{base}/{player}/totals".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url).json()
            gpm = (value['sum'] for value in response if value['field']=='gold_per_min')
            return gpm

        elif field == "xp_per_min":
            url = "{base}/{player}/totals".format(base=DotaRequest.base_url, player=args['player'])
            response = requests.get(url).json()
            xpm = (value['sum'] for value in response if value['field']=='xp_per_min')
            return xpm

        else:
            raise ValueError("{field} is not a valid request".format(field=field))
