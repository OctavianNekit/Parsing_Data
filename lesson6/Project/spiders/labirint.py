import scrapy
from scrapy.http import HtmlResponse
from lesson6.Project.items import ProjectItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/books/']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class = 'pagination-next__text']/@href").extract_first()
        book_links = response.xpath("//div[@class = 'catalog-responsive outer-catalog catalog']"
                                    "//a[@class = 'product-title-link']/@href").extract()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for book_link in book_links:
            yield response.follow(book_link, callback=self.parse_book)

    def parse_book(self, response: HtmlResponse):
        price_sale = None
        price_not_sale = None
        title = response.xpath("//h1").extract_first()
        link = response.url
        if len(title.split(":")) >= 2:
            name = title.split(":")[1]
            author = title.split(":")[0]
        else:
            name = title
            if response.xpath("//a[@data-event-label = 'author']"):
                author = response.xpath("//a[@data-event-label = 'author']/@data-event-content").extract_first()
            else:
                author = None
        currency = response.xpath("//span[@class = 'buying-pricenew-val-currency']").extract_first()
        if response.xpath("//span[@class = 'buying-pricenew-val-number']"):
            price_sale = response.xpath("//span[@class = 'buying-pricenew-val-number']").extract_first() + currency
        if response.xpath("//span[@class = 'buying-priceold-val-number']"):
            price_not_sale = response.xpath("//span[@class = 'buying-priceold-val-number']").extract_first() + currency
        if response.xpath("//span[@class = 'buying-price-val-number']"):
            price_not_sale = response.xpath("//span[@class = 'buying-price-val-number']").extract_first() + currency
        rate = response.xpath("//div[@id = 'rate']").extract_first()
        yield ProjectItem(author=author, name=name, price_sale=price_sale, price_not_sale=price_not_sale, rate=rate, link=link)
