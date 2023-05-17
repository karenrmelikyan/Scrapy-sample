import scrapy


def get_text_by_css(response):
    for quote in response.css('div.quote'):
        first, second = quote.css('span')

        title = first.css('::text').get()
        author = second.css('small::text').get()

        yield {
            'title': title,
            'author': author,
        }


def get_text_by_xpath(response):
    index = 1
    while True:
        title = response.xpath(f'/html/body/div/div[2]/div[1]/div[{index}]/span[1]/text()').get()
        author = response.xpath(f'/html/body/div/div[2]/div[1]/div[{index}]/span[2]/small/text()').get()

        if not title or not author:
            break

        yield {
            'title': title,
            'author': author,
        }

        title = None
        author = None
        index += 1


class QuoteSpider(scrapy.Spider):
    name = "Quote"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):

        index = 1
        while True:
            title = response.xpath(f'/html/body/div/div[2]/div[1]/div[{index}]/span[1]/text()').get()
            author = response.xpath(f'/html/body/div/div[2]/div[1]/div[{index}]/span[2]/small/text()').get()

            if not title or not author:
                break

            yield {
                'title': title,
                'author': author,
            }

            title = None
            author = None
            index += 1

        next_page = response.css('li.next a::attr(href)').get()

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)


