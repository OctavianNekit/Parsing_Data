from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from lesson7.New_Project import settings
from lesson7.New_Project.spiders.Leroy_Merlen import LeroyMerlenSpider

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroyMerlenSpider)
    process.start()
