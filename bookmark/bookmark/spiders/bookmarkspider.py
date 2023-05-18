import scrapy


class BookmarkspiderSpider(scrapy.Spider):
    name = "bookmarkspider"
    allowed_domains = ["bookmark.am"]
    start_urls = ["https://bookmark.am/%D5%A1%D5%BA%D6%80%D5%A1%D5%B6%D6%84%D5%AB-%D5%A2%D5%A1%D5%AA%D5%AB%D5%B6/fiction/"]

    def parse(self, response):
        for books in response.css('div.content-product'):
            yield {
                'title': books.css('h2.product-title a::text').get(),
                'price': books.css('span.woocommerce-Price-amount bdi::text').get().replace("&nbsp;", "").strip(),
                'img': books.css('a.product-content-image::attr(href)').get(),
            }

        next_page = response.css('a.next.page-numbers::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
