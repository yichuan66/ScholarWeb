# download raw information from source, and put them
# into required 'source schema'
#
#   Relevant Information:
#       Scholar Name: str
#       LifeSpan: (int, int)
#       Field: [str] 
#       Influenced by: [str]
#       Influences: [str]
#       MISC information: str

import scrapy
import json
from datetime import datetime

# Source no.1: Wikipedia:
class WikipediaScholarSpider(scrapy.Spider):
    name = 'wiki_scholar'
    start_urls = [
        'https://en.wikipedia.org/wiki/Herbert_A._Simon',
    ]

    def try_parsing_date(self, text):
        year_fmts = ['%y, ', '%y, ', '%Y ', '%Y, ']
        month_fmts = ['%m ', '%m, ', '%b ', '%b, ', '%B ', '%B, ']
        day_fmts = ['%d ', '%d, ']

        orders = [
            [year_fmts, month_fmts, day_fmts],
            [year_fmts, day_fmts, month_fmts],
            [month_fmts, day_fmts, year_fmts],
            [month_fmts, year_fmts, day_fmts],
            [day_fmts, month_fmts, year_fmts],
            [day_fmts, year_fmts, month_fmts],
        ]

        fmts = set()
        for unit_fmts in orders:
            for fmt0 in unit_fmts[0]:
                for fmt1 in unit_fmts[1]:
                    for fmt2 in unit_fmts[2]:
                        fmt = fmt0 + fmt1 + fmt2
                        fmt = fmt.strip(', ')
                        fmts.add(fmt)

        for fmt in fmts:
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                pass

        return None


    def parse(self, response):
    
        result = {}
        result['name'] = response.css('title::text').get().replace(' - Wikipedia', '')
        
        if not result['name'] or result['name'].isspace():
            return

        row_influenced = None
        row_influenced_by = None

        table = response.css('table.biography')
        if not table:
            table = response.css('table.infobox')
        if not table:
            table = response.css('table.vcard')

        for row in table.css('tr'):
            header = row.css('th::text').get()
            
            if header == 'Born' or header == 'Died':
                for val in row.css('td::text').getall():
                    val = str(self.try_parsing_date(val))
                    if val != 'None':
                        val = val.replace('(', '').replace(')', '')
                        result[header.lower()] = val
            elif header == 'Fields':
                result['fields'] = row.css('a::text').getall()
            elif header == 'Influences' or 'Influences' in row.css('div::text').getall():
                result['influenced_by'] = row.css('a::text').getall()
                row_influenced_by = row
            elif header == 'Influenced' or 'Influenced' in row.css('div::text').getall():
                row_influenced = row
                result['influenced'] = row.css('a::text').getall()

        result['misc'] = response.url

        filename = result['name'] + '.json'

        with open('scholars_round4/%s' % filename, 'w') as f:
            f.write(json.dumps(result))

        for item in [row_influenced_by, row_influenced]:
            if item:
                for href in item.css('a::attr(href)'):
                    yield response.follow(href, callback=self.parse)

