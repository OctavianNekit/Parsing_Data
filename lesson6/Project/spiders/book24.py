import scrapy
from scrapy.http import HtmlResponse
from lesson6.Project.items import ProjectItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/knigi-bestsellery/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class = 'pagination__item _link _button _next smartLink']/@href").extract_first()
        book_links = response.xpath("//div[@class = 'product-list__item']"
                                    "//a[@class = 'product-card__name smartLink']/@href").extract()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for book_link in book_links:
            yield response.follow(book_link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        name = response.xpath("//span[@class = 'breadcrumbs__link']/@title").extract_first()
        author = response.xpath("//a[@itemprop = 'author']/text()").extract_first()
        currency = response.xpath("//div[@class = 'item-actions__price']/text()").extract_first()
        if response.xpath("//b[@itemprop = 'price']"):
            price_sale = response.xpath("//b[@itemprop = 'price']/text()").extract_first() + currency
        elif response.xpath("//div[@class = 'item-actions__price']"):
            if response.xpath("//div[@class = 'item-actions__price']/b"):
                price_sale = response.xpath("//div[@class = 'item-actions__price']/b/text()").extract_first() + currency
            else:
                price_sale = response.xpath("//div[@class = 'item-actions__price']/text()").extract_first() + currency
        else:
            price_sale = None
        if response.xpath("//div[@class = 'item-actions__price-old']"):
            price_not_sale = response.xpath("//div[@class = 'item-actions__price-old']/text()").extract_first()
        else:
            price_not_sale = None
        link = response.url
        rate = response.xpath("//div[@class = 'rating__rate-value _bold']/text()").extract_first()
        yield ProjectItem(author=author, name=name, price_sale=price_sale, price_not_sale=price_not_sale, rate=rate, link=link)


