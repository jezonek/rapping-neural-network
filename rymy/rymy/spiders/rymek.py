import scrapy

class QuotesSpider(scrapy.Spider):

    def __init__(self, word =None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.word = word
    name = "rymek"

    def start_requests(self):
        word = getattr(self, "word", None)
        url ='http://rymowanie.pl/rymy/{}/'.format(self.word)
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self,response):
        for rhyme in response.css('.load_word::text').getall():
            yield {'rhyme': rhyme}
