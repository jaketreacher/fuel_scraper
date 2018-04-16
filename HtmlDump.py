import pytz
from datetime import datetime, timedelta


class Table:
    def __init__(self, headings, data):
        self._headings = headings
        self._data = data
        self._tomorrow = (
            datetime.now(pytz.timezone('Australia/Perth'))
            + timedelta(days=1)
        ).date()

    @property
    def headings(self):
        content = ''
        for heading in self._headings:
            content += '<th>' + heading + '</th>'
        return '<tr>' + content + '</tr>'

    @headings.setter
    def headings(self, headings):
        self._headings = headings

    @property
    def data(self):
        content = ''
        for data in self._data:
            date = datetime.strptime(str(data['date']), '%Y-%m-%d').date()
            if date == self._tomorrow:
                content += '<tr class=\'tomorrow\'>'
            else:
                content += '<tr>'
            for heading in self._headings:
                if data[heading]:
                    content += '<td>' + str(data[heading]) + '</td>'
                else:
                    content += '<td></td>'
            content += '</tr>'

        return content

    @data.setter
    def data(self, data):
        self._data = data

    def __str__(self):
        return '<table>' + self.headings + self.data + '</table>'


class HtmlDump:
    def __init__(self, title, headings, data):
        self.title = title
        self.headings = headings
        self.data = data

    def dump(self):
        base = open('templates/base.html').read()
        base = base.replace('{% title %}', self.title)
        table = Table(self.headings, self.data)
        base = base.replace('{% content %}', str(table))
        return base
