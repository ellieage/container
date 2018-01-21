import scrapy


class ContainerSpider(scrapy.Spider):
    name = "container"

    start_urls = [
            # 'https://www.containerstore.com/s/storage/decorative-bins-baskets/12',
            # 'https://www.containerstore.com/s/storage/plastic-bins-baskets/'
            'https://www.containerstore.com/s/storage/'
    ]

    def parse(self, response):
        types = response.xpath('//ul[@class="filter-options three-col-options"]/descendant::a/@href').extract()
        for t in types:
            yield response.follow(t, self.parse_type)

    def parse_type(self, response):
        for href in response.css('.product a::attr(href)'):

            yield response.follow(href, self.parse_container)

        # follow pagination links
        for href in response.css('a.right-arrow-button').xpath('@href'):

            yield response.follow(href, self.parse_type)

    def parse_container(self, response):
        dimensions = response.css('ul.list-stripe li::text').extract()

        if (dimensions==[]):
                dimensions = response.css('.o-block-text--small li::text').extract()
        # price = response.xpath('//div[@itemprop="price"]/text()').extract() # includes $
        price = response.xpath('//div[@itemprop="price"]/@content').extract()
        if (price==[]):
            price = response.xpath('//meta[@itemprop="price"]/@content').extract()
        # image = response.xpath('//a/@data-retina-modal-image').extract()
        # if (image ==[]):
        image = [response.xpath('//ul[@class="o-block-list o-block-list--inline"]/@data-image').extract_first()]
        # image = [response.xpath('//ul[@class="o-block-list o-block-list--inline"]/@data-image').extract_first()]+'/'

        yield {
            'url': response.url,
            'title': response.css('h1::text').extract_first().strip(),
            'dimensions': dimensions,#response.css('.o-block-text--small li::text').extract(),
            'price': price,
            'image': image,
        }




        # # follow pagination links
        # for href in response.css('li.next a::attr(href)'):
        #     yield response.follow(href, self.parse)
