import requests
from lxml import objectify


class FuelWatch:
    baseUrl = 'https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS'
    validKeys = ['product', 'suburb', 'region', 'brand', 'surrounding', 'day']

    def __init__(self):
        self.args = {}

    def set_arg(self, key, value):
        if (key not in self.validKeys):
            raise ValueError("\'%s\' is not a valid key" % key)

        if (key not in self.args):
            self.args[key] = []

        self.args[key].append(value)

    def get_data(self):
        argList = []
        if self.args:
            argList = [combo for combo in self.__generateArgList()]

        items = []
        if argList:
            for args in argList:
                items += self.fetch(args)
        else:
            items += self.fetch()

        return items

    def fetch(self, args=None):
        data = requests.get(self.baseUrl, args)
        xml = objectify.fromstring(data.content)
        items = xml.findall('.//item')

        return items

    def __generateArgList(self, depth=0):
        keys = self.args.keys()
        key = keys[depth]

        max_depth = len(keys)-1
        is_max_depth = depth >= max_depth

        if not is_max_depth:
            for myVal in self.args[key]:
                for argDict in self.__generateArgList(depth+1):
                    argDict[key] = myVal
                    yield argDict
        else:
            for myVal in self.args[key]:
                argDict = {}
                argDict[key] = myVal
                yield argDict
