import scrapy

class QuotesSpider(scrapy.Spider):
    name = "rymek"

    def start_requests(self):
        word = getattr(self, "word", None)
        url ='http://rymowanie.pl/rymy/{}/'.format(word)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        for rhyme in response.css('.load_word::text').getall():
            yield rhyme
