import scrapy
import json
import csv
from zameensite.items import ZameensiteItem


class MyspiderSpider(scrapy.Spider):
    name = "myspider"
    allowed_domains = ["www.zameen.com"]
    start_urls = ["http://www.zameen.com/agents/Lahore-1/?page="]

    def parse(self, response):

        info_nodes = response.xpath("//script[@id='__NEXT_DATA__']/text()").get()
        json_data = json.loads(info_nodes)
        part = response.url.split("page=")[1]
        key = f'getLandingAgencies({{"page":"{part}","q[city_id_in][]":"1","sort":1}})'
        for path in json_data['props']['pageProps']['initialState']['legionApi']['queries'][key]['data']['agencies']:
            item = ZameensiteItem()
            item['estate_name'] = path['name']
            item['mobile_no'] = path['mobile']
            yield item

        next_page_no = json_data['props']['pageProps']['initialState']['legionApi']['queries'][key]['data']['pagination']['next_page']
        if next_page_no:
            next_page_url = f"https://www.zameen.com/agents/Lahore-1/?page={next_page_no}"
            yield scrapy.Request(url=next_page_url,callback=self.parse)
    


