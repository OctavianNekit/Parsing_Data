import scrapy
from scrapy.http import HtmlResponse
from lesson7.New_Project.items import NewProjectItem
from scrapy.loader import ItemLoader


def filter_fun(strings, new):
    for el in strings:
        new_el = el.replace("\n", "")
        new_el = ''.join(new_el.split())
        new.append(new_el)


class LeroyMerlenSpider(scrapy.Spider):
    name = 'Leroy_Merlen'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['https://spb.leroymerlin.ru/catalogue/elektroinstrumenty/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath(
            "//a[@class = 'bex6mjh_plp s15wh9uj_plp l7pdtbg_plp r1yi03lb_plp sj1tk7s_plp']/@href").extract_first()
        goods_links = response.xpath("//a[@class='bex6mjh_plp b1f5t594_plp iypgduq_plp nf842wf_plp']/@href").extract()
        print()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for goods_link in goods_links:
            yield response.follow(goods_link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        loader = ItemLoader(item=NewProjectItem(), response=response)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('photos', '//source[@media=" only screen and (min-width: 1024px)"]/@srcset')
        loader.add_xpath('price', '//span[@slot="price"]/text()')
        loader.add_xpath('currency', '//span[@slot = "currency"]/text()')
        loader.add_value('link', response.url)
        parameters = response.xpath('//dt[@class="def-list__term"]/text()').extract()
        old_meaning = response.xpath('//dd[@class = "def-list__definition"]/text()').extract()
        new_mean = []
        filter_fun(old_meaning, new_mean)
        loader.add_value('info', dict(zip(parameters, new_mean)))
        yield loader.load_item()
