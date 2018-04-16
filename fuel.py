from FuelWatch import FuelWatch
from HtmlDump import HtmlDump

myWatch = FuelWatch()
myWatch.set_arg('Day', ['today', 'tomorrow'])
data = myWatch.get_data()
data = sorted(data, key=lambda k: k['price'])

kwargs = {
    'title': 'Fuel Scraper',
    'headings': ['brand', 'address', 'date', 'price'],
    'data': data
}

html = HtmlDump(**kwargs)
open('index.html', 'w').write(html.dump())
