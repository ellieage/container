import scrapy


class ContainerSpider(scrapy.Spider):
    name = "container"

    start_urls = [
            'https://www.containerstore.com/s/storage/decorative-bins-baskets/',
            'https://www.containerstore.com/s/storage/plastic-bins-baskets/'
    ]

    def parse(self, response):

        for href in response.css('.product a::attr(href)'):
            yield response.follow(href, self.parse_container)

        # follow pagination links
        for href in response.css('a.right-arrow-button').xpath('@href'):
            # print('\n ----------------------------------------- \n new page \n' + str(href.extract()) + '\n')
            yield response.follow(href, self.parse)

    def parse_container(self, response):
        dimensions = response.css('.o-block-text--small li::text').extract()
        if (dimensions==[]):
            dimensions = response.css('ul.list-stripe li::text').extract()
        # price = response.xpath('//div[@itemprop="price"]/text()').extract() # includes $
        price = response.xpath('//div[@itemprop="price"]/@content').extract()
        if (price==[]):
            price = response.xpath('//meta[@itemprop="price"]/@content').extract()

        yield {
            'url': response.url,
            'title': response.css('h1::text').extract_first().strip(),
            'dimensions': dimensions,#response.css('.o-block-text--small li::text').extract(),
            'price': price
        }




        # # follow pagination links
        # for href in response.css('li.next a::attr(href)'):
        #     yield response.follow(href, self.parse)
