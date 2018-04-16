import requests
from lxml import objectify


class FuelWatch:
    baseUrl = 'https://www.fuelwatch.wa.gov.au/fuelwatch/fuelWatchRSS'
    validKeys = ['Product', 'Suburb', 'Region', 'Brand', 'Surrounding', 'Day']

    def __init__(self):
        self.args = {}

    def set_arg(self, key, value):
        if (key not in self.validKeys):
            raise ValueError("\'%s\' is not a valid key" % key)

        self.args[key] = value if type(value) is list else list(value)

    def get_data(self):
        argList = []
        if self.args:
            argList = [combo for combo in self.__generateArgList()]

        items = []
        if argList:
            for args in argList:
                items += self.__fetch(args)
        else:
            items += self.__fetch()

        return items

    def __fetch(self, args=None):
        data = requests.get(self.baseUrl, params=args)
        xml = objectify.fromstring(data.content)
        items = xml.findall('.//item')

        return items

    def __generateArgList(self, depth=0):
        keys = sorted(self.args.keys())
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
