import scrapy


class ContainerSpider_ikea(scrapy.Spider):
    name = "container_ikea"

    start_urls = [
            # 'http://www.ikea.com/us/en/catalog/products/20110540/' # a specific container
            'http://www.ikea.com/us/en/catalog/categories/departments/secondary_storage/10550/'
    ]

    def parse(self, response):

        for href in response.xpath('//div[contains(@id, "item")]/div/a/@href').extract():

            yield response.follow(href, self.parse_container)

    def parse_container(self, response):
        dimensions = []
        dimensions = response.xpath('//div[@id="productDimensionsContainer"]').xpath('//div[@id="imperial"]/text()').extract()
        if dimensions[0].split()==[]:
            dimensions=[]

            dim_try = response.xpath('//div[@id="goodToKnow"]/text()').extract()
            if 'Sizes' in dim_try[0]:
                dim_text = dim_try[0]
                for r in dim_text.split():
                    if 'x' in r:
                        dimensions.append(r)


            elif 'Sizes' in dim_try[1]:
                dim_text = dim_try[1]

                for r in dim_text.split():
                    if 'x' in r:
                        dimensions.append(r)

        price = [response.xpath('//span[contains(@id, "schemaProductPrice")]/@content').extract_first()]
        image = ['http://www.ikea.com'+response.xpath('//img[contains(@id, "productImg")]/@src').extract_first()]

        yield {
            'url': response.url,
            'title': response.css('title::text').extract_first().strip(),
            'dimensions': dimensions,
            'price': price,
            'image': image
        }
