import scrapy
from scrapy.crawler import CrawlerProcess


class AuthorsSpider(scrapy.Spider):
    name = "authors"
    custom_settings = {"FEED_FORMAT": "json", "FEED_URI": "authors.json", 'FEED_EXPORT_ENCODING': 'utf-8',
                       'FEED_EXPORT_INDENT': 4}
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com"]

    def parse(self, response):
        for author in response.xpath("/html//small[@class='author']"):
            # Павук провалюється на сторінку автора
            author_url = response.urljoin(author.xpath("../a/@href").get())
            yield scrapy.Request(url=author_url, callback=self.parse_author_info)

            next_link = response.xpath("//li[@class='next']/a/@href").get()
            if next_link:
                yield response.follow(next_link, self.parse)

    def parse_author_info(self, response):
        yield {
            "fullname": response.xpath("//h3[@class='author-title']/text()").get(),
            "born_date": response.xpath("//p/span[@class='author-born-date']/text()").get(),
            "born_location": response.xpath("//p/span[@class='author-born-location']/text()").get(),
            "description": response.xpath("//div[@class='author-description']/text()").get()
        }




# run spider
process = CrawlerProcess()
process.crawl(AuthorsSpider)
process.start()
